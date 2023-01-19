from behave import then, when, given
from BDDCommon.CommonConfigs.locatorsconfig import CART_PAGE_LOCATORS
from BDDCommon.CommonFuncs import webcommon
import logging as logger
import time


@when("I select 'Free shipping' option")
def i_select_free_shipping_option(context):
    """

    """
    logger.info("")
    logger.info("")
    logger.info("33333")
    logger.info("About to select the free shipping option")
    free_ship = CART_PAGE_LOCATORS['free_shipping_radio']
    webcommon.click(context, free_ship['type'], free_ship['locator'])

    webcommon.assert_radio_is_selected(context, free_ship['type'], free_ship['locator'])
    logger.info("Successfully selected the free shipping option")

@when("I click on 'Proceed to checkout' button in the cart page")
def i_click_on_proceed_to_checkout_button_in_the_cart_page(context):
    """

    """
    proceed_button = CART_PAGE_LOCATORS['proceed_to_checkout_btn']

    max_try = 3
    try_count = 0
    while try_count < max_try:
        try:
            webcommon.click(context, proceed_button['type'], proceed_button['locator'])
            break
        except Exception as e:
            try_count += 1
            print(f"Failed to click on 'Proceed to checkout' Retry number: {try_count}")
    else:
        raise Exception(f"Failed to click on 'Proceed to checkout' after retrying '{max_try}' times.")


@when("I get the total dollar amount of the cart")
def i_get_the_total_dollar_amount_of_the_cart(context):
    time.sleep(2)
    total_locator = CART_PAGE_LOCATORS['total_cart_value']

    total_raw = webcommon.get_element_text(context, total_locator['type'], total_locator['locator'])
    context.cart_total = total_raw.replace('$', '')


@when("I apply the coupon to the cart")
def i_apply_the_coupon_to_the_cart(context):

    coupon_field_locator = CART_PAGE_LOCATORS['coupon_code_field']
    apply_coupon_locator = CART_PAGE_LOCATORS['apply_coupon_button']

    webcommon.type_into_element(context, context.coupon_code, coupon_field_locator['type'], coupon_field_locator['locator'])
    webcommon.click(context, apply_coupon_locator['type'], apply_coupon_locator['locator'])


@then("the total should be reduced by {pct}%")
def the_total_should_be_reduced_by_pct(context, pct):

    original_total = context.cart_total
    expected_new_total = float(original_total) * (float(pct)/100)

    context.execute_steps("when I get the total dollar amount of the cart")
    new_total = context.cart_total

    assert float(new_total) == expected_new_total, \
        f"Cart total after applying {pct}% coupon is not as expected." \
        f"Original: {original_total}, Expected: {expected_new_total}, Actual: {new_total}"

