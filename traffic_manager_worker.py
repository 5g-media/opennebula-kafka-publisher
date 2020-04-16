import json
import logging.config
import time
import schedule
from kafka import KafkaProducer
from kafka.errors import KafkaError
from settings import LOGGING, KAFKA_API_VERSION, KAFKA_SERVER, XML_RPC_SERVER, XML_RPC_SESSION, NO_OSM_VM_IDS, \
    KAFKA_TRAFFIC_MANAGER_TOPIC, KAFKA_TRAFFIC_SCHEDULER_SECONDS
from xmlrpc_api.one_vm_info import OneVMInfo
from xmlrpc_api.parser import export_data_from_one_vm_info
from utils import convert_unix_timestamp_to_datetime_str, get_unit_by_metric, convert_bytes_to_bits

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)

TX_PREVIOUS_STATE = {'tx_bytes': None, 'timestamp': None}
RX_PREVIOUS_STATE = {'rx_bytes': None, 'timestamp': None}


def main():
    """ Publish the VNFs related metrics in the KAFKA_OPENNEBULA_TOPIC while
    the ones coming from standalone VMs such as the Traffic Manager in the KAFKA_TRAFFIC_MANAGER_TOPIC

    Returns:
        None
    """
    producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER, api_version=KAFKA_API_VERSION,
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    # Consider also the VMs, not spawn by OSM
    no_osm_vm_ids = []
    for vm_id in NO_OSM_VM_IDS.split(','):
        if not len(vm_id):
            continue
        no_osm_vm_ids.append(vm_id)

    for vm_id in no_osm_vm_ids:
        # Get the info of the VM by given session and VM id
        one_vm_info = OneVMInfo()
        response = one_vm_info.get(XML_RPC_SERVER, XML_RPC_SESSION, vm_id)
        raw_response = response.text

        # Parse the response and keep the monitoring metrics as a dict
        monitoring_info, last_poll = export_data_from_one_vm_info(raw_response)

        if last_poll is None:
            logger.warning("The last poll is {}".format(last_poll))
            return

        # Convert the unix time in UCT iso8601 format
        timestamp = convert_unix_timestamp_to_datetime_str(float(last_poll))

        for metric, value in monitoring_info.items():
            metric_type = metric.lower()
            payload = {"vdu_uuid": vm_id, "type": metric_type, "value": value,
                       "unit": get_unit_by_metric(metric_type), "timestamp": timestamp}
            publish_metric(producer, payload)

            try:
                if metric_type == 'nettx':
                    logger.info(TX_PREVIOUS_STATE)
                    if TX_PREVIOUS_STATE['timestamp'] is not None:
                        old_tx = convert_bytes_to_bits(int(TX_PREVIOUS_STATE['tx_bytes']))
                        new_tx = convert_bytes_to_bits(int(value))
                        seconds = int(last_poll) - int(TX_PREVIOUS_STATE['timestamp'])
                        logger.debug('Seconds among poll: {}'.format(seconds))
                        if seconds != 0:
                            tx_kbps = (new_tx - old_tx) * pow(10, -3) / seconds
                            payload = {"vdu_uuid": vm_id, "type": 'tx_kbps', "value": tx_kbps,
                                       "unit": 'kbps', "timestamp": timestamp}
                            logger.debug(payload)
                            publish_metric(producer, payload)
                    TX_PREVIOUS_STATE['timestamp'] = last_poll
                    TX_PREVIOUS_STATE['tx_bytes'] = value
                elif metric_type == 'netrx':
                    logger.debug(RX_PREVIOUS_STATE)
                    if RX_PREVIOUS_STATE['timestamp'] is not None:
                        old_rx = convert_bytes_to_bits(int(RX_PREVIOUS_STATE['rx_bytes']))
                        new_rx = convert_bytes_to_bits(int(value))
                        seconds = int(last_poll) - int(RX_PREVIOUS_STATE['timestamp'])
                        logger.debug('Seconds among poll: {}'.format(seconds))
                        if seconds != 0:
                            rx_kbps = (new_rx - old_rx) * pow(10, -3) / seconds
                            payload = {"vdu_uuid": vm_id, "type": 'rx_kbps', "value": rx_kbps,
                                       "unit": 'kbps', "timestamp": timestamp}
                            logger.debug(payload)
                            publish_metric(producer, payload)
                    RX_PREVIOUS_STATE['timestamp'] = last_poll
                    RX_PREVIOUS_STATE['rx_bytes'] = value
            except Exception as e:
                logger.exception(e)

    producer.close()


def publish_metric(producer, metric):
    # Publish the metric
    request = producer.send(KAFKA_TRAFFIC_MANAGER_TOPIC, metric)
    try:
        # set timeout in 5 sec
        request.get(timeout=5)
    except KafkaError as ke:
        logger.error(ke)


if __name__ == '__main__':
    # Retrieve the data every X seconds
    schedule.every(int(KAFKA_TRAFFIC_SCHEDULER_SECONDS)).seconds.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
