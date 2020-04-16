import logging.config
from settings import LOGGING
from httpclient.client import Client

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class OneVMMonitoring(object):
    """
    See Also: https://docs.opennebula.org/5.6/integration/system_interfaces/api.html
    """

    def __init__(self):
        """Constructor of OneVMMonitoring class"""
        self.__client = Client(verify_ssl_cert=False)
        self.method = "one.vm.monitoring"
        self.headers = {"Content-Type": "application/xml"}

    def get(self, url, session, vm_id):
        """ Get the VM monitoring info

        Args:
            url (str): the url of the XML-RPC API of OpenNebula
            session (str): the OpenNebula session
            vm_id (int): the VM id

        Returns:
            object: the requests object
        """
        payload = """<?xml version='1.0'?>
            <methodCall>
            <methodName>{}</methodName>
            <params>
            <param>
            <value><string>{}</string></value>
            </param>
            <param>
            <value><int>{}</int></value>
            </param>
            </params>
            </methodCall>""".format(self.method, session, vm_id)
        response = self.__client.post(url, payload=payload, headers=self.headers)
        return response
