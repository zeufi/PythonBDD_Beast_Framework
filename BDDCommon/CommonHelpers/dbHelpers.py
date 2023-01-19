
import pymysql
from BDDCommon.CommonHelpers.credentialsHelper import CredentialsHelper
import os
from BDDCommon.CommonConfigs.hosts_config import DB_HOST


class DBHelpers(object):
    def __init__(self):
        credentials_helper = CredentialsHelper()
        self.credentials = credentials_helper.get_db_credentials()

        self.machine = os.environ.get('MACHINE')
        assert self.machine, f"Environment variable 'MACHINE' must be set."

        self.wp_host = os.environ.get('WP_HOST')
        assert self.wp_host, f"Environment variable 'WP_HOST' must be set."

        if self.machine == 'docker' and self.wp_host == 'local':
            raise Exception(f"Can not run test in docker if WP_HOST=local")

        self.env = os.environ.get('ENV', 'test')

        self.host = DB_HOST[self.machine][self.env]['host']
        self.socket = DB_HOST[self.machine][self.env]['socket']
        self.port = DB_HOST[self.machine][self.env]['port']
        self.database = DB_HOST[self.machine][self.env]['database']
        self.table_prefix = DB_HOST[self.machine][self.env]['table_prefix']

    def create_connection(self):

        if self.wp_host == 'local':
            connection = pymysql.connect(host=self.host, user=self.credentials['db_user'],
                                         password=self.credentials['db_password'],
                                         unix_socket=self.socket)
        elif self.wp_host == 'ampps':
            connection = pymysql.connect(host=self.host, user=self.credentials['db_user'],
                                         password=self.credentials['db_password'],
                                         port=self.port)
        else:
            raise Exception("Unknown WP_HOST.")

        return connection

    def execute_select(self, sql):
        conn = self.create_connection()
        try:
            self.create_connection()
            cur = conn.cursor(pymysql.cursors.DictCursor)
            cur.execute(sql)
            rs_dict = cur.fetchall()
            cur.close()
        except Exception as e:
            raise Exception("Failed running sql {}. Error: {}".format(sql, str(e)))
        finally:
            conn.close()

        return rs_dict

    def execute_sql(self):
        pass
