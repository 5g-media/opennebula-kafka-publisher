import xmltodict
import logging
from settings import LOGGING
from exceptions import OneVmInfoException, OneVmMonitoringException

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


def export_data_from_one_vm_info(data):
    """ Export the monitoring metrics from the one.vm.info function for one timestamp.

    See Also: https://docs.opennebula.org/5.6/integration/system_interfaces/api.html

    Args:
        data (xml): the response body as it is provided from the one.vm.info request.

    Returns:
        tuple (dict, str): the monitoring metrics and the last poll (unix time)

    Examples:
        (
            {
              "CPU": "0.0",
              "DISKRDBYTES": "349236528",
              "DISKRDIOPS": "54146",
              "NETTX": "648",
              "DISKWRBYTES": "1798374400",
              "STATE": "a",
              "DISKWRIOPS": "16832",
              "MEMORY": "673188",
              "NETRX": "4830677802"
            },
            '1553834036'
        )

    """
    last_poll = None
    monitoring_info = {}

    try:
        response = xmltodict.parse(data)
        response_value = response["methodResponse"].get("params", {}).get("param", {}).get("value", {}). \
            get("array", {}).get("data", {}).get("value", [])

        for record in response_value:
            if 'string' in record.keys():
                xml_info = record['string']
                vm_info = xmltodict.parse(xml_info)
                # Get the monitoring entries and convert the order dict to dict
                last_poll = vm_info.get('VM', {}).get('LAST_POLL', None)
                monitoring_info = dict(vm_info.get('VM', {}).get('MONITORING', {}))
                if 'DISK_SIZE' in monitoring_info:
                    del monitoring_info['DISK_SIZE']
                break
    except OneVmInfoException as ex:
        logger.exception(ex)
    finally:
        return monitoring_info, last_poll


def export_metrics_from_one_vm_monitoring(data):
    """ Export the monitoring metrics from the one.vm.monitoring function in `batch`.

    See Also: https://docs.opennebula.org/5.6/integration/system_interfaces/api.html

    Args:
        data (xml): the response body as it is provided from the one.vm.info request.

    Returns:
        list: A list of dicts that includes the metrics per given timestamp (unix_time)

    Examples:
        [
            {
                "metrics": {
                    "CPU": "0.0",
                    "DISKRDBYTES": "349236528",
                    "DISKRDIOPS": "54146",
                    "NETTX": "648",
                    "DISKWRBYTES": "1798374400",
                    "STATE": "a",
                    "DISKWRIOPS": "16832",
                    "MEMORY": "673188",
                    "NETRX": "4830677802"
                },
                "last_poll": "1553834036"
            }
        ]
    """
    monitoring_data = []

    try:
        response = xmltodict.parse(data)
        response_value = response["methodResponse"].get("params", {}).get("param", {}).get("value", {}). \
            get("array", {}).get("data", {}).get("value", [])

        # We pick the 2nd entry
        record = response_value[1]
        xml_info = record['string']
        vm_info = xmltodict.parse(xml_info)
        mon_data = vm_info['MONITORING_DATA']
        entries = mon_data['VM']

        for entry in entries:
            monitoring_info = dict(entry.get('MONITORING', {}))
            # Exclude the disk size
            if 'DISK_SIZE' in monitoring_info:
                del monitoring_info['DISK_SIZE']
            monitoring_data.append({"metrics": monitoring_info, "last_poll": entry.get('LAST_POLL', None)})
    except OneVmMonitoringException as e:
        logger.exception(e)
    finally:
        return monitoring_data
