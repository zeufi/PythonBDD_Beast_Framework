
from BDDCommon.CommonHelpers.dbHelpers import DBHelpers
import random


class ProductsDAO(object):

    def __init__(self):
        self.db_heler = DBHelpers()

    def get_app_products_from_db(self):

        sql = "SELECT * FROM mystore.wp_posts WHERE post_type = 'product';"
        rs_sql = self.db_heler.execute_select(sql)
        return rs_sql

    def get_random_products_from_db(self, qty):

        sql = "SELECT * FROM mystore.wp_posts WHERE post_type = 'product' ORDER BY id DESC LIMIT 5000;"
        rs_sql = self.db_heler.execute_select(sql)
        return random.sample(rs_sql, int(qty))
