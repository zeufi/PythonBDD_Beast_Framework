
from BDDCommon.CommonHelpers.dbHelpers import DBHelpers


class OrdersDAO(object):

    def __init__(self):
        self.db_heler = DBHelpers()

    def get_order_by_id(self, order_id):

        sql = "SELECT * FROM mystore.wp_posts WHERE ID = {};".format(order_id)

        return self.db_heler.execute_select(sql)
