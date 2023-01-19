from behave import step
from BDDCommon.CommonConfigs.locatorsconfig import HOME_PAGE_LOCATORS
from BDDCommon.CommonFuncs import webcommon
import random
import time
import logging as logger


@step("I add {qty} random item to cart from the homepage")
def i_add_random_item_to_cart_from_the_homepage(context, qty):
    logger.info("1111")
    logger.info(f"Adding {qty} items to cart")

    cart_btns = HOME_PAGE_LOCATORS['all_add_cart_btns']
    cart_btns_type = cart_btns['type']
    cart_btns_text = cart_btns['locator']

    cart_btns = webcommon.find_elements(context, cart_btns_type, cart_btns_text)
    random_btns = random.sample(cart_btns, int(qty))

    for i in random_btns:
        webcommon.click(i)
    time.sleep(1)


@step("I click on cart in the top nav bar and verify cart page opens")
def i_click_on_cart_in_the_top_nav_bar_and_verify_cart_page_opens(context):
    cart_info_locator = HOME_PAGE_LOCATORS['cart_info_box']
    webcommon.click(context, cart_info_locator['type'], cart_info_locator['locator'])
    webcommon.assert_url_contains(context, '/cart/')
