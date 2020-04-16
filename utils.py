from datetime import datetime, timedelta
import urllib.parse
from dateutil import tz
from nbi_api import identity, vim_account, vnf
from settings import METRICS_LIST


def convert_unix_timestamp_to_datetime_str(unix_ts):
    """ Convert a unix timestamp in stringify datetime (UTC)

    Args:
        unix_ts (float): The timestamp in unix

    Returns:
        str: The datetime in str (UTC)

    Example:
        >>> from datetime import datetime
        >>> from utils import convert_unix_timestamp_to_datetime_str
        >>> unix_ts = 1527165350
        >>> dt_str = convert_unix_timestamp_to_datetime_str(unix_ts)
        >>> print(dt_str)
        2018-05-24T12:35:50.000000Z
    """
    dt = datetime.utcfromtimestamp(unix_ts)
    return dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')


def get_unit_by_metric(metric):
    """ Get the unit by given metric

    Args:
        metric (str): The metric name

    Returns:
        str: the unit
    """
    for item in METRICS_LIST:
        if item['name'] == metric:
            return item['unit']
    return ""


def get_type_by_metric(metric):
    """ Get the type by given metric

    Args:
        metric (str): The metric name

    Returns:
        str: the metric's type
    """
    for item in METRICS_LIST:
        if item['name'] == metric:
            return item['type']
    return ""


def get_opennebula_vim_uuid(token):
    """ Fetch the uuid of the OpenNebula VIM

    Args:
        token (str): the token of the NBI API

    Returns:
        str: the OpenNebula VIM uuid. None if not found.
    """
    vim = vim_account.VimAccount(token)
    request = vim.get_list()
    vims = request.json()
    for item in vims:
        vim_type = item.get('vim_type', None)
        if vim_type is None:
            continue
        if vim_type == "opennebula":
            return item.get("_id", None)
    return None


def get_opennebula_vm_ids(token, vim_uuid):
    """ Fetch the VM ids hosted in the OpenNebula VIM

    Args:
        token (str): the token of the NBI API
        vim_uuid(str): the OpenNebula VIM uuid

    Returns:
        list: the list of VM ids
    """
    vm_ids = []

    vnf_obj = vnf.Vnf(token)
    request = vnf_obj.get_list()
    vnfs = request.json()

    for item in vnfs:
        vim_account_id = item.get("vim-account-id", None)
        if vim_account_id != vim_uuid:
            continue

        vdurs = item.get("vdur", [])
        for vdur in vdurs:
            try:
                vm_id = int(vdur.get("vim-id"))
                vm_ids.append(vm_id)
            except Exception as ex:
                pass

    return vm_ids


def convert_bytes_to_bits(_bytes):
    """ Convert bytes to bits

    Args:
        bytes : The RX or TX bytes

    Returns:
        int: bits
    """
    if bytes is None:
        return None
    return int(_bytes) * 8
