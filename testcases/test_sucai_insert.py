from  libs.common_request import HttpRequest
import allure
import pytest
from libs.mySql import MySql_connect as m
from libs.common_uploadImg import pcPost_upload
import random as r


filename1 = 'D:\\PyCharmProject\\dj_api_test\\image2.png'
filename2 = 'D:\\PyCharmProject\\dj_api_test\\image.png'

@allure.epic('产品管理')
@allure.feature('素材管理')
@pytest.mark.dj_pc_goods
class TestSuCaiInsert():
    @allure.story('新增素材')
    @allure.title('新增素材->成功')
    def test_sucai_insert(self,login):

       with  allure.step('步骤1：先获取缩略图图片地址'):
           data1={
               'method':'dj.api.common.uploadImg'
           }
           res1=pcPost_upload('/rop-dj-smartcarlife/router',data=data1,file=filename1)
           assert res1.status_code == 200 ,'预期status_code与实际不一致'
           assert res1.json()['code'] == '0','预期code与实际不一致'
           assert res1.json()['message'] == '调用服务成功!','预期message与实际不一致'

           thumbUrl = res1.json()['data']

       with  allure.step('步骤2：先获取产品主图图片地址'):
           data2={
               'method':'dj.api.common.uploadImg'
           }
           res2=pcPost_upload('/rop-dj-smartcarlife/router',data=data2,file=filename2)
           assert res2.status_code == 200 ,'预期status_code与实际不一致'
           assert res2.json()['code'] == '0','预期code与实际不一致'
           assert res2.json()['message'] == '调用服务成功!','预期message与实际不一致'

           goodsImg = res2.json()['data']

       # 随机素材名
       first_name = ["朗逸汽车保养", "轩逸汽车保养", "长安汽车保养", "名爵汽车保养", "哈佛汽车保养", '雅阁汽车保养', '思域汽车保养']
       secod_name = ['1', '2', '3', '4', '5', '6', '7']
       goodsname = r.choice(first_name) + ''.join(r.choice(secod_name))

       with allure.step('步骤3：新增工单'):
            data = {
                'merchantId':'44211025',
                'goodsName': goodsname,
                'goodsType': '1',
                'goodsTypeName': '太阳膜',
                'sapCode': '10011',
                'brandMerchantCode': '1',
                'brandMerchantName': '3M/福膜',
                'thumbUrl': thumbUrl,
                'thumbUrlList[0].content': thumbUrl,
                'goodsImgList[0].content': goodsImg,
                'goodsDescList[0].resType': '2',
                'goodsDescList[0].orderNo': '0',
                'goodsDescList[0].content': '覆盖到梵蒂冈吧',
                'method': 'dj.api.goodsinfo.add',
                'sessionId': login
            }

            res = HttpRequest.dj_post('/rop-dj-smartcarlife/router',data)
            print(res.json())

            #assert  res.json()['data'] == 201,'预期id与实际不一致'
            assert  res.json()['data']['goodsName'] == goodsname,'预期goodsName与实际不一致'

       with allure.step('步骤4：界面查询工单成功'):
           params ={

               'pageSize':'20',
               'currentPage': '1',
               'goodsName': goodsname,
               'method': 'dj.api.goodsinfo.page',
               'sessionId': login
           }
           res = HttpRequest.dj_get('/rop-dj-smartcarlife/router',params)
           assert  res.json()['data']['list'][0]['goodsName'] == goodsname,'预期goodsName与实际不一致'
























