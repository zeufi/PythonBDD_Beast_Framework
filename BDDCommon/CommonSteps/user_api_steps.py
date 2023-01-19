from behave import step
from BDDCommon.CommonHelpers.utilitiesHelpers import generate_random_email_and_password
from BDDCommon.CommonAPI import user_api
from BDDCommon.CommonDAO.usersDAO import UsersDAO


@step("I generate random email and password")
def i_generate_random_email_and_password(context):

    random_info = generate_random_email_and_password()
    context.random_email = random_info['email']
    context.random_password = random_info['password']


@step("I call 'create customer' api")
def i_call_create_customer_api(context):
    payload = {'email': context.random_email, 'password': context.random_password}

    create_user_response = user_api.create_user(data=payload)
    assert create_user_response, "Empty response for create user. Payload: {}".format(payload)
    assert create_user_response['email'] == context.random_email, \
        "Wrong email in response of 'create user' api." \
        "Call email: {}, response email: {}".format(
        context.random_email, create_user_response['email'])

    expected_user_name = context.random_email.split('@')[0]
    assert create_user_response['username'] == expected_user_name, \
        "Wrong 'username' in response of 'create user' api." \
        "Call username: {}, response username: {}".format(
        expected_user_name, create_user_response['username'])


@step("customer should be created")
def customer_should_be_created(context):
    db_user = UsersDAO().get_user_by_email(context.random_email)

    assert len(db_user) == 1, "Find user in db by email found {} resulsts. " \
                              "Email: {}".format(len(db_user), context.random_email)
    expected_user_name = context.random_email.split('@')[0]
    assert db_user[0]['user_login'] == expected_user_name, \
        "User created in db does not have the expected user name. " \
        "Exptected: {}, Actual: {}".format(expected_user_name, db_user[0]['user_login'])
