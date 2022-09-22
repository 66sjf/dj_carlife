import  pytest
import  allure
from  libs.common_request import  HttpRequest
from  libs.mySql import MySql_connect

@allure.feature('订单管理')
@pytest.mark.dj_pc_order
class TestOrder():

    @allure.story('订单列表')
    @allure.title('通过客户姓名查询')
    @pytest.mark.flaky(reruns=2,reruns_delay=3) #失败重跑1次，等待3s
    #@pytest.mark.order  # 打上order标签，调用pytest.ini文件
    def test_order_select_by_customerName_success(self,login):
        """
        场景1：
        通过客户姓名查询
        """
        with allure.step('步骤1:先拿到登录sessionid,游标对象'):
            sessionid =login  #根据装饰器获取sessionid
            conn,cur=MySql_connect().connect() #接收数据库对象，游标对象


        with allure.step('步骤2：输入测试数据'):
            params = {
                'customerName': '看看',
                'method': 'dj.api.smartcarlife.ordermanage.page',
                'pageNum':'1',
                'pageSize':'20',
                'sessionId': sessionid
            }
        with allure.step('步骤3：调用请求方法，获得响应数据'):
            res = HttpRequest.dj_get('/rop-dj-smartcarlife/router',params)

        with allure.step('步骤4：进行其他的断言（除状态码，code,message外）'):



            #进行total断言，预期结果与实际结果进行对比
            assert  res.json()['data']['total'] == 2,'预期total的值与实际值不一致'

            #customerName断言
            assert  res.json()['data']['list'][0]['customerName'] == '看看'



    @allure.story('订单列表')
    @allure.title('通过商品名称查询')
    #@pytest.mark.order  # 打上order标签，调用pytest.ini文件
    def test_order_select_by_goodsName_success(self,login):
        """
        场景2：
        通过商品名称查询
        :return:
        """
        with allure.step('步骤1：获得登录sessionid'):
            sessionid = login # 根据装饰器获取sessionid

        with allure.step('步骤2：输入测试数据'):
            params = {
                'orderGoodsName': '发件地',
                'method': 'dj.api.smartcarlife.ordermanage.page',
                'sessionId': sessionid,
                'pageNum': '1',
                'pageSize': '20'

            }

        with allure.step('步骤3：调用请求方法，获得响应数据'):
            res = HttpRequest.dj_get('/rop-dj-smartcarlife/router',params)

        with allure.step('步骤4：进行其他的断言（除状态码，code,message外）'):



            # 进行total断言，预期结果与实际结果进行对比
            assert res.json()['data']['total'] == 33, '预期total的值与实际值不一致'

            # orderCode断言
            assert res.json()['data']['list'][0]['orderCode'] == '2208241416083166','预期orderCode的值与实际值不一致'

    @allure.story('订单列表')
    @allure.title('通过订单状态查询')
    #@pytest.mark.order  # 打上order标签，调用pytest.ini文件
    def test_order_select_by_orderStatus_success(self,login):
        """
        场景3：
        通过订单状态查询
        :return:
        """
        with allure.step('步骤1：获得登录sessid'):
            sessionid = login  # 根据装饰器获取sessionid


        with allure.step('步骤2：输入测试数据'):
            params = {
                'status': '4',
                'method': 'dj.api.smartcarlife.ordermanage.page',
                'sessionId': sessionid,
                'pageNum': '1',
                'pageSize': '20'

            }

        with allure.step('步骤3：调用请求方法，获得响应数据'):
            res = HttpRequest.dj_get('/rop-dj-smartcarlife/router',params)

        with allure.step('步骤4：进行其他的断言（除状态码，code,message外）'):

            # 进行total断言，预期结果与实际结果进行对比
            assert res.json()['data']['total'] == 137, '预期total的值与实际值不一致'

            # status断言
            assert res.json()['data']['list'][0]['status'] == 4,'预期status的值与实际值不一致'



if __name__ == '__main__':
    t = TestOrder()
    t.test_order_select_by_customerName_success()

