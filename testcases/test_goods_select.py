
from  libs.common_request import  HttpRequest
import  pytest
import  allure
from  libs.mySql import MySql_connect


@allure.feature('产品管理')
@pytest.mark.dj_pc_goods
class TestGoods():

    @allure.story('零售商品')
    @allure.title('通过商品名称查询')
    def test_goods_select_by_goodsName(self,login):
        """
        场景1 通过商品名称查询
        :return:
        """
        with allure.step('步骤1：获取登录sessionid，获得数据库游标'):
            sessionid = login
            conn,cur =MySql_connect.connect()

        with allure.step('步骤2：测试数据，查询数据库'):
            params = {
                'pageSize':'20',
                'currentPage': '1',
                'goodsName': '预约有',
                'method': 'dj.api.basegoods.page',
                'sessionId': sessionid,
            }

            sql = """select * from dj_car_life_goods_info where id <5"""
            cur.execute(sql)
            #data = cur.fetchall() #获取全部的表数据
            datas = cur.fetchone() #获取一条数据
            print('------------')
            print(datas)


        with allure.step('步骤3：调用请求方法，获得响应数据'):
            res = HttpRequest.dj_get('/rop-dj-smartcarlife/router',params)

        with allure.step('步骤4：进行断言操作'):

            # total断言
            assert  res.json()['data']['total'] == 1 ,'toatal的值与预期不一致'

            #goodsName断言
            assert res.json()['data']['list'][0]['goodsInfo']['goodsName'] == '预约有' ,'goodsName的值与预期不一致'

    @allure.story('零售商品')
    @allure.title('通过产品状态查询')
    def test_goods_select_by_status(self, login):
        """
        场景1 通过产品状态查询
        :return:
        """
        with allure.step('步骤1：获取登录sessionid'):
            sessionid = login

        with allure.step('步骤2：测试数据'):
            params = {
                'pageSize': '20',
                'currentPage': '1',
                'status': '1',
                'method': 'dj.api.basegoods.page',
                'sessionId': sessionid,
            }
        with allure.step('步骤3：调用请求方法，获得响应数据'):
            res = HttpRequest.dj_get('/rop-dj-smartcarlife/router', params)

        with allure.step('步骤4：进行断言操作'):

            # total断言
            assert res.json()['data']['total'] == 15, 'toatal的值与预期不一致'

            # goodsName断言
            assert res.json()['data']['list'][0]['goodsCode'] == 'M210219175725846', 'goodsCode的值与预期不一致'


if __name__ == '__main__':
    conn, cur = MySql_connect.connect()
    sql = """select * from dj_car_life_goods_info where id <5"""
    cur.execute(sql)
    datas = cur.fetchall() #获取全部的表数据
    #data = cur.fetchone()  # 获取一条数据
    print('------------')
    #print(datas)
    for data in datas:
        print(data)
