import pymysql

class Mysql_Connection():
    """
    连接数据库
    """
    def __init__(self,host,port,user,password,db):
        """
        初始化基本参数
        :param host: 数据库地址
        :param port: 端口号
        :param user: 用户名
        :param password: 密码
        :param db: 连接数据库名
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        #self.charset = 'utf-8'

    def conn_success(self):
        """
        数据库连接成功
        :return:
        """
        #第一步：连接
        conn = pymysql.connect(
            host = self.host,
            port = self.port,
            user = self.user,
            password = self.password,
            database = self.db,
            #charset = 'utf-8'
        )
        #第二步:获得游标对象
        cur = conn.cursor()
        #print(cur)
        return  cur,conn #返回游标、连接

    def insert_sql(self):
        """
        向表中插入数据
        :return:
        """
        #
        try:
            sql = 'insert into platform_merchant_login(user_type)'
            cur,conn = self.conn_success()
            insert = cur.execute(sql) #执行语句
            print('插入成功')
        except:
            print('数据插入异常！')
        else:
            conn.commit(insert) #提交插入的数据
            self.close_mysql() #关闭操作

    def select_sql(self):
        """
        查询表中的数据
        :return:
        """
        try:
            cur,conn = self.conn_success()
            sql = 'select * from platform_merchant_login where login_accout = \'aa123456\' '
            cur.execute(sql)
        except:
            print('查询记录为空！')
        else:
            result = cur.fetchall()
            #print(f'数据查询成功{result}')
            for res in result:
                #print(res)
                print(f'数据查询成功，id是：{res[0]}   账户名是：{res[2]}')

            self.close_mysql() #关闭库
            return  result


    def close_mysql(self):
        """
        关闭游标、数据库连接
        :return:
        """
        cur,conn = self.conn_success() #初始化数据库连接

        cur.close() #关闭游标

        conn.close() #关闭数据库连接


if __name__ == '__main__':
    m = Mysql_Connection('192.168.1.39',3306,'insurance_user','123456','scrm_account')
    #m.conn_success()
    print(m.select_sql())
