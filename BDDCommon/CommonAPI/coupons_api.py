from BDDCommon.CommonHelpers.wooRequestHelpers import WooRequestsHelper


def create_coupon(data):
    return WooRequestsHelper().post('coupons', data, expected_status_code=201)