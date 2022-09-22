import  allure
import  pytest
from libs.common_request import HttpRequest
from  libs.mySql import MySql_connect


@allure.epic('产品管理')
@allure.feature('素材管理')
@pytest.mark.dj_pc_goods
class TestSucaiDelete():
    @allure.story('删除素材')
    @allure.title('删除素材->成功')
    def test_sucai_delete(self,login):
        """
        删除素材
        :param login:
        :return:
        """
        with allure.step('步骤1：删除素材，选择是'):
            data = {
                'goodsCode': 'M220916175751387',
                'method': 'dj.smartcarlife.api.goodsinfo.checkDeleteable',
                'sessionId': login
            }
            res = HttpRequest.dj_post('/rop-dj-smartcarlife/router', data)

            assert res.json()['data'] == True, '预期True与实际不一致'

        with allure.step('步骤2：删除素材成功'):
            data = {
                'goodsCode':'M220916175751387',
                'method':'dj.smartcarlife.api.goodsinfo.delete',
                'sessionId':login
            }
            res = HttpRequest.dj_post('/rop-dj-smartcarlife/router',data)

            assert res.json()['data']['id'] == None,'预期id与实际不一致'

        with allure.step('步骤3：删除后查询数据库数据'):
            conn,cur=MySql_connect.connect()
            sql = """select * from dj_car_life_goods_info where goods_code = 'M220916175751387' """
            cur.execute(sql)
            datas = cur.fetchone()
            assert  datas['deleted_flag'] == 'D'


