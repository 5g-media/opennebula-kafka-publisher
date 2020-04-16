import requests
from .baseclient import AbstractClient
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()


class Client(AbstractClient):
    def __init__(self, verify_ssl_cert=False):
        self.verify_ssl_cert = verify_ssl_cert
        super(Client, self).__init__()

    def post(self, url, headers=None, payload=None, **kwargs):
        """Insert an entity.

        Args:
            url (str): the endpoint of the web service
            headers (dict): the required HTTP headers, e.g., Accept: application/json
            payload (str): the xml payload
            kwargs (dict, optional): Additional arguments will be passed to the request.

        Returns:
            obj: a requests object
        """
        response = requests.request("POST", url, data=payload, headers=headers, verify=self.verify_ssl_cert)
        return response
