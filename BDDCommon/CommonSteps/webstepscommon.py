
from behave import given, then, step
from BDDCommon.CommonFuncs import webcommon

# start of step definitions


@step("I go to '{page}' page")
@given('I go to the site "{page}"')
def go_to_page(context, page):
    """
    Step definition to go to the specified url.
    :param context:
    :param page:
    """

    print("Navigating to the page: {}".format(page))
    webcommon.go_to(context, page)


# ========================================================================================#
@then('the page title should be "{expected_title}"')
def verify_homepage_title(context, expected_title):
    """
    Verifies the home page title is as expected.
    :param context:
    :param expected_title:
    :return:
    """

    webcommon.assert_page_title(context, expected_title)


# ========================================================================================#
@then('current url should be "{expected_url}"')
def verify_current_url(context, expected_url):
    """
    Verifies the current uls is as expected_url
    :param context:
    :param expected_url:
    """
    webcommon.assert_current_url(context, expected_url)
