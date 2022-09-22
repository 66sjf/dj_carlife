"""
@Description: 
@Author: Lzc
@Time: 2022/8/3 18:00
@File: finance_list_test.py
"""

import pytest
import allure
from lib.request import HttpRequest
from random import randint,choice
import requests
from lib.router import smartcarlife
from time import sleep
from pprint import pprint



@allure.feature('产品管理')
@allure.story('素材管理')
@pytest.mark.dj_admin
@pytest.mark.dj_admin_product
class TestMaterial(HttpRequest):
    """
    素材管理-素材的增删改查相关测试场景
    """


    @allure.title('产品管理—>素材管理->新增素材->成功')
    def test_create_material(self, admin_login):
        """
        附加了查询、修改和删除的操作
        :param admin_login:
        :return:
        """
        _, sid = admin_login

        # 上传缩略图与产品主图
        data = {
            'method': 'dj.api.common.uploadImg',
            'sessionId': sid,
        }

        self.r = self.wpost_upload(smartcarlife, data, file='resource/image/a.png')
        self.common_assert()
        self.assert_in('data', '.png')
        self.assert_in('data', 'http:')
        thumb_url = self.r.json().get('data')

        data = {
            'method': 'dj.api.common.uploadImg',
            'sessionId': sid,
        }

        self.r = self.wpost_upload(smartcarlife, data, file='resource/image/b.png')
        self.common_assert()
        self.assert_in('data', '.png')
        self.assert_in('data', 'http:')
        goods_img_url = self.r.json().get('data')

        name = f'lzc牛皮脚垫{randint(1,99999)}'
        # 创建素材
        data = {
            'method': 'dj.api.goodsinfo.add',
            'merchantId': '44184606',
            'goodsName': name,
            'goodsType': '2',
            'goodsTypeName': '脚垫',
            'thumbUrl': thumb_url,
            'thumbUrlList[0].content': thumb_url,
            'goodsImgList[0].content': goods_img_url,
            'sessionId': sid,
        }

        self.r = self.wpost(smartcarlife, data)
        self.common_assert()
        self.assert_type('data.id', int)
        material_id = self.r.json().get('data').get('id')

        # 根据名称查询素材
        data = {
            'method': 'dj.api.goodsinfo.page',
            'pageSize': '20',
            'currentPage': '1',
            'goodsName': name,
            'sessionId': sid,
        }
        self.r = self.wget(smartcarlife, data)

        ### assertion & extract ###
        self.common_assert()
        self.assert_equal('data.total', 1)
        # 产品主图信息
        goods = self.r.json()['data']['list'][0]
        goods_img_info = goods['goodsImgList'][0]
        # 删除用
        goods_code = goods['goodsCode']
        ### assertion & extract ###


        # 导出

        # 修改素材(修改名称)
        new_name = '新' + name
        data = {
            'method': 'dj.api.goodsinfo.update',
            'merchantId': '44184606',
            'id': material_id,
            'goodsName': new_name,
            'goodsType': '2',
            'goodsTypeName': '脚垫',
            'thumbUrl': thumb_url,
            'goodsImgList[0].id': goods_img_info['id'],
            'goodsImgList[0].goodsCode': goods_img_info['goodsCode'],
            'goodsImgList[0].content': goods_img_info['content'],
            'goodsImgList[0].resType': goods_img_info['resType'],
            'goodsImgList[0].bizType': goods_img_info['bizType'],
            'goodsImgList[0].orderNo': goods_img_info['orderNo'],
            'goodsImgList[0].createdBy': 'glsadmin',
            'goodsImgList[0].updatedBy': 'glsadmin',
            'goodsImgList[0].deletedFlag': 'N',
            'sessionId': sid,
        }

        self.r = self.wpost(smartcarlife, data)
        self.common_assert()
        self.assert_equal('data.id', material_id)
        self.assert_equal('data.goodsName', new_name)

        # 删除素材
        # check delete
        data = {
            'method': 'dj.smartcarlife.api.goodsinfo.checkDeleteable',
            'goodsCode': goods_code,
            'sessionId': sid,
        }
        self.r = self.wpost(smartcarlife, data)
        self.common_assert()
        self.assert_equal('data', True)
        # delete
        data = {
            'method': 'dj.smartcarlife.api.goodsinfo.delete',
            'goodsCode': goods_code,
            'sessionId': sid,
        }
        self.r = self.wpost(smartcarlife, data)
        self.common_assert()
        self.assert_equal('data.id', None)

    @allure.title('产品管理—>素材管理->(按分类)查询->成功')
    def test_query_material_1(self, admin_login):
        """
        产品管理—>素材管理->(按分类)查询->成功
        """
        _, sid = admin_login

        #
        data = {
            'method': 'dj.api.goodsinfo.page',
            'pageSize': '20',
            'currentPage': '1',
            'goodsType': '2',
            'sessionId': sid,
        }

        self.r = self.wget(smartcarlife, data)
        self.common_assert()
        self.assert_ge('data.total', 1)
        for i in self.r.json()['data']['list']:
            assert i['goodsType'] == 2, f"{i['goodsType']} != 2"

    @allure.title('产品管理—>素材管理->(按创建时间)查询->成功')
    def test_query_material_2(self, admin_login):
        """
        产品管理—>素材管理->(按创建时间)查询->成功
        """
        _, sid = admin_login

        #
        data = {
            'method': 'dj.api.goodsinfo.page',
            'pageSize': '20',
            'currentPage': '1',
            # 下面两个参数，蔡远明反馈说：前端自己传的，没什么用
            # 'createTime[0]': '2022-06-30T16:00:00.000Z',
            # 'createTime[1]': '2022-08-28T16:00:00.000Z',
            'startDate': '2022-7-1 00:00:00',
            'endDate': '2022-8-29 23:59:59',
            'sessionId': sid,
        }

        self.r = self.wget(smartcarlife, data)
        self.common_assert()
        self.assert_ge('data.total', 1)

    @allure.title('产品管理—>素材管理->(按品牌商)查询->成功')
    def test_query_material_3(self, admin_login):
        """
        产品管理—>素材管理->(按品牌商)查询->成功
        """
        _, sid = admin_login

        #
        data = {
            'method': 'dj.api.goodsinfo.page',
            'pageSize': '20',
            'currentPage': '1',
            # 3M/福膜
            'brandMerchantCode': '1',
            'sessionId': sid,
        }

        self.r = self.wget(smartcarlife, data)
        self.common_assert()
        self.assert_ge('data.total', 1)
        return

    @allure.title('产品管理—>素材管理->(按素材名称)查询->成功')
    def test_query_material_4(self, admin_login):
        """
        产品管理—>素材管理->(按素材名称)查询->成功
        """
        _, sid = admin_login

        #
        data = {
            'method': 'dj.api.goodsinfo.page',
            'pageSize': '20',
            'currentPage': '1',
            'goodsName': '小鸭子',
            'sessionId': sid,
        }

        self.r = self.wget(smartcarlife, data)
        self.common_assert()
        self.assert_equal('data.total', 1)

    @allure.title('产品管理—>素材管理->导出->成功')
    def test_material_export(self, admin_login):
        """
        产品管理—>素材管理->导出->成功
        """
        _, sid = admin_login

        #
        data = {
            'method': 'dj.api.common.async.exportExcel',
            'exportParam': '{"goodsName":"小鸭子","method":"dj.api.goodsinfo.export.async"}',
            'sessionId': sid,
        }

        self.r = self.wget(smartcarlife, data)
        self.common_assert()
        file_uuid = self.r.json().get('data')
        sleep(1.5)
        while True:
            sleep(0.5)
            data = {
                'method': 'dj.api.common.query.async.exportExcel',
                'fileUuidList[0]': file_uuid,
                'sessionId': sid,
            }
            self.r = self.wget(smartcarlife, data)
            self.common_assert()
            file_info = self.r.json().get('data')[0]
            if file_info.get('status') == 1:
                file_url = file_info.get('fileUrl')
                break
        self.r = requests.get(url=file_url)
        assert self.r.status_code == 200, f'状态码错误，实际值{self.r.status_code}'
        self.assert_content_type('application/octet-stream')
