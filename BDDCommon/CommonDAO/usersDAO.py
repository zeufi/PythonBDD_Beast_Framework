
from BDDCommon.CommonHelpers.dbHelpers import DBHelpers


class UsersDAO(object):

    def __init__(self):
        self.db_heler = DBHelpers()

    def get_user_by_email(self, email):

        sql = "SELECT * FROM mystore.wp_users WHERE user_email = '{}';".format(email)

        return self.db_heler.execute_select(sql)
