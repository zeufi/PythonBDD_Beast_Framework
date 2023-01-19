
from BDDCommon.CommonHelpers.wooRequestHelpers import WooRequestsHelper


def create_user(data):

    return WooRequestsHelper().post(wc_endpoint='customers', params=data, expected_status_code=201)
