from woocommerce import API
from BDDCommon.CommonHelpers.credentialsHelper import CredentialsHelper
import logging as logger


class WooRequestsHelper(object):

    def __init__(self):
        credentials_helper = CredentialsHelper()
        wc_credentials = credentials_helper.get_wc_api_keys()

        self.wc_api = API(
            url="http://192.168.1.183:8888/Mystore",
            consumer_key=wc_credentials['wc_key'],
            consumer_secret=wc_credentials['wc_secret'],
            version="wc/v3"
        )

    def assert_status_code(self):
        assert self.rs.status_code == self.expected_status_code, \
            "Bad status code. Endpoint: {}, Params: {}. " \
            "Actual status code: {}, Expected status code: {}, " \
            "Response body: {}".format(
                self.wc_endpoint, self.params, self.rs.status_code,
                self.expected_status_code, self.rs.json())

    def get(self, wc_endpoint, params=None, expected_status_code=200):
        self.rs = self.wc_api.get(wc_endpoint, params=params)
        self.wc_endpoint = wc_endpoint
        self.expected_status_code = expected_status_code
        self.params = params
        self.assert_status_code()
        return self.rs.json()

    def post(self, wc_endpoint, params=None, expected_status_code=200):
        logger.info(f"Params: {params}")
        self.rs = self.wc_api.post(wc_endpoint, data=params)
        self.wc_endpoint = wc_endpoint
        self.expected_status_code = expected_status_code
        self.params = params
        self.assert_status_code()
        return self.rs.json()

    def delete(self):
        pass

    def put(self):
        pass


if __name__ == '__main__':
    myObj = WooRequestsHelper()
    # myObj.get("products")

    payload = {
        "email": "dummyemail2@supersqa.com",
        "password": "123abc"
    }

    response = myObj.post("customers", params=payload, expected_status_code=201)
    import pprint
    pprint.pprint(response)
