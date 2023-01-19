import time
from behave import *
from BDDCommon.CommonFuncs import webcommon
from BDDCommon.CommonConfigs.locatorsconfig import MY_ACCOUNT_LOCATORS


@step("I type '{email}' into username of login form")
def type_email_into_username_of_login_form(context, email):
    """
    :param context:
    :param email:
    :return:
    """
    time.sleep(2)
    email_locator_type = MY_ACCOUNT_LOCATORS['login_user_name']['type']
    email_locator_string = MY_ACCOUNT_LOCATORS['login_user_name']['locator']
    webcommon.type_into_element(context, email, email_locator_type, email_locator_string)


@step("I type '{password}' into password of login form")
def type_password_into_password_of_login_form(context, password):
    """
    :param password:
    :param context:
    :return:
    """
    time.sleep(2)
    pass_locator_type = MY_ACCOUNT_LOCATORS['login_user_password']['type']
    pass_locator_string = MY_ACCOUNT_LOCATORS['login_user_password']['locator']
    webcommon.type_into_element(context, password, pass_locator_type, pass_locator_string)


@step("I click on the '{btn_name}' button")
def i_click_on_the_login_button(context, btn_name):
    """
    :param context:
    :param btn_name:
    :return:
    """
    time.sleep(2)
    if btn_name.lower() in ('login', 'log in'):
        login_btn_locator_type = MY_ACCOUNT_LOCATORS['login_btn']['type']
        login_btn_locator_string = MY_ACCOUNT_LOCATORS['login_btn']['locator']
    else:
        raise Exception("Not implemented")
    webcommon.click(context, login_btn_locator_type, login_btn_locator_string)


@step("user should be logged in")
def user_should_be_logged_in(context):
    """
    :param context:
    :return:
    """
    time.sleep(2)
    nav_bar_type = MY_ACCOUNT_LOCATORS['left_nav']['type']
    nav_bar_text = MY_ACCOUNT_LOCATORS['left_nav']['locator']

    logout_type = MY_ACCOUNT_LOCATORS['left_nav_logout_btn']['type']
    logout_text = MY_ACCOUNT_LOCATORS['left_nav_logout_btn']['locator']

    webcommon.assert_element_visible(context, nav_bar_type, nav_bar_text)
    webcommon.assert_element_visible(context, logout_type, logout_text)


@then("error message with email '{email}' should be displayed")
def error_message_with_email_should_be_displayed(context, email):
    """
    :param context:
    :param email:
    :return:
    """
    time.sleep(2)
    expected_msg = "Error: The password you entered for the email address {email} is incorrect. Lost your " \
                   "password?".format(email=email)

    error_box_type = MY_ACCOUNT_LOCATORS['error_box']['type']
    error_box_text = MY_ACCOUNT_LOCATORS['error_box']['locator']

    is_exist = webcommon.element_contains_text(context, expected_msg, error_box_type, error_box_text)

    if is_exist:
        print('Pass')
    else:
        raise Exception("Correct error message not displayed at failed login. Email: {}".format(email))


@then("error message with 'Unknown email' should be displayed")
def error_message_with_unknown_email_should_be_displayed(context):
    """
    :param context:
    :return:
    """
    time.sleep(2)
    expected_msg = "Unknown email address. Check again or try your username."
    error_box_type = MY_ACCOUNT_LOCATORS['error_box']['type']
    error_box_text = MY_ACCOUNT_LOCATORS['error_box']['locator']

    is_exist = webcommon.element_contains_text(context, expected_msg, error_box_type, error_box_text)
    if is_exist:
        print('Pass')
    else:
        raise Exception("Correct error message not displayed at failed login. None existing email: {}")
