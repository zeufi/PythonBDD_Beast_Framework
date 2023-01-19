from behave import step
from BDDCommon.CommonHelpers.utilitiesHelpers import generate_random_coupon_code
from BDDCommon.CommonAPI import coupons_api
from BDDCommon.CommonDAO.couponsDAO import CouponsDAO
import json





@step('I create a "{discount_type}" coupon')
def create_a_coupon_with_given_discount_type(context, discount_type):
    data = {
        "code": generate_random_coupon_code(),
    }
    if discount_type.lower() != 'none':
        context.expected_discount_type = discount_type
        data["discount_type"] = discount_type
    else:
        context.expected_discount_type = 'fixed_cart'

    rs_api = coupons_api.create_coupon(data)

    context.new_coupon_info = rs_api


@step("the coupon should exist in database")
def the_coupon_should_exist_in_database(context):
    coupon_dao = CouponsDAO()

    coupon_id = context.new_coupon_info['id']
    db_coupon = coupon_dao.get_coupon_by_id(coupon_id)
    assert db_coupon, f'Coupon not found in database. Coupon id: {coupon_id}'

    coupon_meta = coupon_dao.get_coupon_metadata_by_id(coupon_id)
    assert coupon_meta['discount_type'] == context.expected_discount_type, \
        f"Unexpected 'discount_type' for new coupon. " \
         f"Expected: {context.expected_discount_type}, Actual: {coupon_meta['discount_type']}"


@step("I create a coupon with given parameters")
def i_create_a_coupon_with_given_parameters(context):

    data_raw = context.text
    data = json.loads(data_raw)
    data['code'] = generate_random_coupon_code()

    rs_api = coupons_api.create_coupon(data)

    context.new_coupon_info = rs_api


@step("I verify the given metadata in database")
def i_verify_the_given_metadata_in_database(context):

    expected_values_raw = context.text
    expected_values = json.loads(expected_values_raw)

    coupon_id = context.new_coupon_info['id']
    db_meta = CouponsDAO().get_coupon_metadata_by_id(coupon_id)

    failed_fields = []
    for key, value in expected_values.items():
        if str(db_meta[key]) != str(value):
            failed_fields.append(
                {
                key: {'expected': value,
                     'db': db_meta[key]}
                }
            )

    if failed_fields:
        raise Exception(f"Metadata when creating coupon unexpected. Failed fields: {failed_fields}")

@step("I get a valid {pct}% off coupon")
def i_get_a_valid_pct_coupon(context, pct):
    # Option 1: get it from db
    # Option 2: create a new one, and delete at teardown
    # Option 3: hard code a coupon that will not expire or run out

    if int(pct) == 50:
        context.coupon_code = "TEST50"
    else:
        raise Exception("Not implemented")

