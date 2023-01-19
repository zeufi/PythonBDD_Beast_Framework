from behave import when
from BDDCommon.CommonConfigs.locatorsconfig import CHECKOUT_PAGE_LOCATORS
from BDDCommon.CommonFuncs import webcommon
from BDDCommon.CommonHelpers.utilitiesHelpers import generate_random_email_and_password
from BDDCommon.CommonHelpers.utilitiesHelpers import generate_random_first_and_last_names

@when("I verify 'Checkout' page is loaded")
def i_verify_checkout_page_is_loaded(context):
    """

    """

    # check the url
    webcommon.assert_url_contains(context, '/checkout/')

    # check the heading text
    expected_text = 'Checkout'
    header_locator = CHECKOUT_PAGE_LOCATORS['page_header']
    contains = webcommon.element_contains_text(context, expected_text, header_locator['type'], header_locator['locator'])
    assert contains, f"Header of checkout page does not contain the text '{expected_text}'."

    # check some elements are visible
    form_locator = CHECKOUT_PAGE_LOCATORS['checkout_form']
    webcommon.assert_element_visible(context, form_locator['type'], form_locator['locator'])

    # import pdb; pdb.set_trace()

@when("I fill in the billing details form")
def i_fill_in_the_billing_details_form(context):
    rand_name = generate_random_first_and_last_names()
    f_name = rand_name['f_name']
    l_name = rand_name['l_name']
    addr_1 = '123 Main st.'
    city = 'San Francisco'
    _zip = 94111
    phone = '5101111111'
    email = generate_random_email_and_password()['email']

    f_name_locator = CHECKOUT_PAGE_LOCATORS['billing_f_name_input']
    l_name_locator = CHECKOUT_PAGE_LOCATORS['billing_l_name_input']
    street_locator = CHECKOUT_PAGE_LOCATORS['billing_address1_input']
    city_locator = CHECKOUT_PAGE_LOCATORS['billing_city_input']
    zip_locator = CHECKOUT_PAGE_LOCATORS['billing_zip_input']
    phone_locator = CHECKOUT_PAGE_LOCATORS['billing_phone_input']
    email_locator = CHECKOUT_PAGE_LOCATORS['billing_email_input']

    # start input the values
    webcommon.type_into_element(context, f_name, f_name_locator['type'], f_name_locator['locator'])
    webcommon.type_into_element(context, l_name, l_name_locator['type'], l_name_locator['locator'])
    webcommon.type_into_element(context, addr_1, street_locator['type'], street_locator['locator'])
    webcommon.type_into_element(context, city, city_locator['type'], city_locator['locator'])
    webcommon.type_into_element(context, _zip, zip_locator['type'], zip_locator['locator'])
    webcommon.type_into_element(context, phone, phone_locator['type'], phone_locator['locator'])
    webcommon.type_into_element(context, email, email_locator['type'], email_locator['locator'])



@when("I click on 'Place order' button in the checkout page")
def i_click_on_place_order_button_in_the_checkout_page(context):

    btn_locator = CHECKOUT_PAGE_LOCATORS['place_order_btn']
    webcommon.click(context, btn_locator['type'], btn_locator['locator'])
