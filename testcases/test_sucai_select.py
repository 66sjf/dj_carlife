from  libs.common_request import HttpRequest
import allure
import pytest
from libs.mySql import MySql_connect as m



@allure.epic('产品管理')
@allure.feature('素材管理')
@pytest.mark.dj_pc_goods
class TestSuCaiSelect():

    @allure.story('查询')
    @allure.title('通过素材名称')
    def test_sucai_select_by_goodsName(self,login):
        """
        场景1：通过素材名称查询
        :return:
        """
        with allure.step('步骤1：获取登录sessionid'):
            sessionid = login

        with allure.step('步骤2：测试数据'):
            params = {
                'goodsName': '我哦哦',
                'method': 'dj.api.goodsinfo.page',
                'currentPage': '1',
                'pageSize': '20',
                'sessionId': sessionid
            }

        with allure.step('步骤3：调用请求接口，获得响应数据'):
            res = HttpRequest.dj_get('/rop-dj-smartcarlife/router',params)

        with allure.step('步骤4：断言操作'):

            #total断言
            assert  res.json()['data']['total'] == 1 ,'预期total的值与实际值不一致'

            #goodsName断言
            assert  res.json()['data']['list'][0]['goodsName'] == '我哦哦'


        with allure.step('步骤5：数据库表数据与界面数据对比'):
            conn,cur =m.connect()
            sql = """ select * from dj_car_life_goods_info where  goods_name = '我哦哦'"""
            cur.execute(sql)
            data=cur.fetchone() #获取一条信息
            #data = cur.fetchall()
            print(data)

            assert  data['id'] == 162,'预期id的值与实际值不一致'

            assert  data['goods_name'] == '我哦哦','预期goods_name的值与实际值不一致'
            conn.close()

    @allure.story('查询')
    @allure.title('通过素材分类')
    def test_sucai_select_by_goodsType(self,login):
        with allure.step('步骤1：获取查询数据，并进行断言操作'):
            params={

                'goodsType': '1',
                'method': 'dj.api.goodsinfo.page',
                'currentPage': '1',
                'pageSize': '20',
                'sessionId': login
            }

            res = HttpRequest.dj_get('/rop-dj-smartcarlife/router',params)

            #assert res.json()['data']['total'] == 6,'预期total与实际不一致'

            assert  res.json()['data']['list'][0]['goodsType'] ==1,'预期goodsType与实际不一致'

        with allure.step('步骤2：界面数据与数据库表数据进行校验'):
            conn,cur = m.connect()

            sql = """select * from dj_car_life_goods_info where  goods_Type =1"""
            cur.execute(sql)
            datas = cur.fetchall()
            for data in datas:
                assert  data['goods_type'] == 1,'预期goods_Type与实际不一致'

                assert  data['goods_type_name'] == '太阳膜','预期goods_Type与实际不一致'
            conn.close()

    @allure.story('查询')
    @allure.title('通过品牌商')
    def test_sucai_select_by_brandMerchantCode(self,login):
        with allure.step('步骤1：获取查询数据，并进行断言操作'):
            params = {
                'brandMerchantCode': '1',
                'method': 'dj.api.goodsinfo.page',
                'currentPage': '1',
                'pageSize': '20',
                'sessionId': login
            }
            res = HttpRequest.dj_get('/rop-dj-smartcarlife/router',params)
            #断言时，如果发现时间条数与抓包不一样时，对比登录账户，不同账户可见的范围不一样
            #assert res.json()['data']['total'] == 2,'预期total与实际不一致'
            assert res.json()['data']['list'][0]['brandMerchantName'] == '3M/福膜','预期brandMerchantName与实际不一致'
            assert res.json()['data']['list'][0]['brandMerchantCode'] == '1','预期brandMerchantCode与实际不一致'

        with allure.step('步骤2：界面数据与数据库表数据进行校验'):
            conn,cur =m.connect()
            sql = """select * from dj_car_life_goods_info where brand_merchant_code=1 and merchant_id=44211025"""
            cur.execute(sql)
            data = cur.fetchone()
            #print(data['id'])
            assert  data['id'] == 127 ,'预期id与实际不一致'
            assert  data['brand_merchant_name'] == '3M/福膜','预期brandMerchantName与实际不一致'
            conn.close()


    @allure.story('查询')
    @allure.title('通过创建时间')
    def test_sucai_select_by_createTime(self,login):
        with allure.step('步骤1：获取查询数据，并进行断言操作'):
            params = {

                'createTime[0]': '2022-06-30T16:00:00.000Z',
                'createTime[1]': '2022-07-29T16:00:00.000Z',
                'startDate': '2022-7-1 00:00:00',
                'endDate': '2022-7-30 23:59:59',
                'method': 'dj.api.goodsinfo.page',
                'currentPage': '1',
                'pageSize': '20',
                'sessionId': login
            }
            res = HttpRequest.dj_get('/rop-dj-smartcarlife/router',params)
            assert  res.json()['data']['total'] == 2,'预期total与实际不一致'
            assert  res.json()['data']['list'][0]['id'] == 164,'预期id与实际不一致'
            assert res.json()['data']['list'][1]['id'] == 163, '预期id与实际不一致'

        with allure.step('步骤2：界面数据与数据库表数据进行校验'):
            conn,cur = m.connect()
            sql = """select * from dj_car_life_goods_info where  created_date>='2022-7-1 00:00:00'and created_date <='2022-7-30 23:59:59' and merchant_id=44211025"""
            cur.execute(sql)
            datas = cur.fetchall()
            for data in datas:
                print(data)
                if data['id'] == 163:
                    assert  data['goods_name'] == '测试ERP物料1' , '预期goods_name与实际不一致'
                elif data['id'] == 164:
                    assert data['goods_name'] == '测试无编号素材', '预期goods_name与实际不一致'
            conn.close()









