import string
import random


def generate_random_email_and_password(domain=None, email_prefix=None):

    if not domain:
        domain = 'supersdet.com'
    if not email_prefix:
        email_prefix = 'testuser'

    random_email_string_length = 10
    random_string = ''.join(random.choices(string.ascii_lowercase, k=random_email_string_length))

    email = email_prefix + '_' + random_string + '@' + domain

    password_length = 20
    password_string = ''.join(random.choices(string.ascii_letters, k=password_length))
    random_info = {'email': email, 'password': password_string}
    print("")
    print("Random email and password: {}".format(random_info))
    return random_info


def generate_random_first_and_last_names(f_name_pre='test f ', l_name_pre='test l '):

    random_f_name = f_name_pre + ''.join(random.choices(string.ascii_lowercase, k=7))
    random_l_name = l_name_pre + ''.join(random.choices(string.ascii_lowercase, k=7))
    return {'f_name': random_f_name, 'l_name': random_l_name}


def generate_random_coupon_code(sufix=None, length=10):

    code = ''.join(random.choices(string.ascii_uppercase, k=length))
    if sufix:
        code += sufix
    return code
