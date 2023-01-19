
from BDDCommon.CommonHelpers.dbHelpers import DBHelpers
import logging as logger


class CouponsDAO(object):

    def __init__(self):
        self.db_heler = DBHelpers()

    def get_coupon_by_id(self, coupon_id):

        sql = f'SELECT * FROM mystore.wp_posts WHERE ID = {coupon_id} AND post_type = "shop_coupon";'

        return self.db_heler.execute_select(sql)

    def get_coupon_metadata_by_id(self, coupon_id):
        sql = f'SELECT * FROM mystore.wp_postmeta WHERE post_id = {coupon_id};'
        rs_sql = self.db_heler.execute_select(sql)

        logger.debug(f"")
        logger.debug(f"SQL Result: \n {rs_sql}")
        logger.debug(f"")

        coupon_meta = dict()
        for i in rs_sql:
            coupon_meta[i['meta_key']] = i['meta_value']

        return coupon_meta
