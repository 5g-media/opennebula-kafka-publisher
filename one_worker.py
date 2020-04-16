import json
import logging.config
import time
import schedule
from kafka import KafkaProducer
from kafka.errors import KafkaError
from nbi_api import identity
from utils import get_opennebula_vim_uuid, get_opennebula_vm_ids
from settings import LOGGING, SCHEDULER_MINUTES, KAFKA_API_VERSION, KAFKA_SERVER, KAFKA_OPENNEBULA_TOPIC, \
    XML_RPC_SERVER, XML_RPC_SESSION, OSM_ADMIN_CREDENTIALS
from xmlrpc_api.one_vm_info import OneVMInfo
from xmlrpc_api.parser import export_data_from_one_vm_info
from utils import convert_unix_timestamp_to_datetime_str, get_unit_by_metric

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


def main():
    """ Publish the VNFs related metrics in the KAFKA_OPENNEBULA_TOPIC while
    the ones coming from standalone VMs such as the Traffic Manager in the KAFKA_TRAFFIC_MANAGER_TOPIC

    Returns:
        None
    """

    producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER, api_version=KAFKA_API_VERSION,
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    # Get the UUID of the OpenNebula VIM
    token = identity.bearer_token(OSM_ADMIN_CREDENTIALS.get('username'), OSM_ADMIN_CREDENTIALS.get('password'))
    one_vim_uuid = get_opennebula_vim_uuid(token)

    # Get the list of VM ids of the OpenNebula NSs
    vm_ids = get_opennebula_vm_ids(token, one_vim_uuid)
    logger.info('The list of VMs {} have been detected given the VIM uuid `{}``'.format(vm_ids, one_vim_uuid))

    # Get the metrics for each running VM in OpenNebula instantiated due to the OSM
    for vm_id in vm_ids:
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

            # Publish the metric
            request = producer.send(KAFKA_OPENNEBULA_TOPIC, payload)
            try:
                # set timeout in 5 sec
                request.get(timeout=5)
            except KafkaError as ke:
                logger.error(ke)
    producer.close()


if __name__ == '__main__':
    # Retrieve the data every X minutes
    schedule.every(int(SCHEDULER_MINUTES)).minutes.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
