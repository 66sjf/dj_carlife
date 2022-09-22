import pymysql
class MySql_connect():

    @staticmethod
    def connect():
        """
        连接数据库
        :return:
        """
        conn = pymysql.connect(
            host='192.168.1.39',
            port=3306,
            user='insurance_user',
            password='123456',
            db='dj_smartcarlife',
            charset='utf8')
        cur = conn.cursor(pymysql.cursors.DictCursor) #获得游标对象，pymysql.cursors.DictCursor 把获取到的数据转化为字典格式

        return  conn,cur

    @staticmethod
    def close_mysql():
        """
        关闭操作
        :return:
        """
        conn,cur=MySql_connect.connect()
        conn.close() #关闭数据库连接
        cur.close() #关闭游标对象





