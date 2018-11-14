'''
'''
from pymysql import connect as my_connect
from pymysql import cursors as cursors
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column, Date, Integer, String, ForeignKey


class db(object):
    @property
    def ENGINE_MYSQL_hawaii(self):
        return create_engine("mysql+pymysql://:/",connect_args={'charset': 'utf8'})
    @property
    def ENGINE_MYSQL_duckchat(self):
        return create_engine("mysql+pymysql://::@",connect_args={'charset': 'utf8'})
    @property
    def ENGINE_MARIADB_dw(self):
        return create_engine("mysql+pymysql://:@/dw",connect_args={'charset': 'utf8'})
    @property
    def CONN_MYSQL_hawaii(self):
        return my_connect(host='',user='root',password='',port=3306, database='',charset='utf8mb4')
    @property
    def CONN_MYSQL_duckchat(self):
        return my_connect(host='',user='',password='',port=3306, database='',charset='utf8mb4', cursorclass=cursors.SSDictCursor)
    @property
    def MetaData_MYSQL_hawaii(self):
        return  MetaData(self.ENGINE_MYSQL_hawaii)
    @property
    def MetaData_MYSQL_duckchat(self):
        return  MetaData(self.ENGINE_MYSQL_duckchat)   
    @property
    def MetaData_IMPALA_DW(self):
        return  MetaData(self.ENGINE_IMPALA_DW)

if __name__ == '__main__':
    pass
    # user_table = Table('dw_derivative_mx', MetaData_IMPALA_DW, autoload=True)



