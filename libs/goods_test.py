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
@allure.story('零售商品')
@pytest.mark.dj_admin
@pytest.mark.dj_admin_product
class TestCommodity(HttpRequest):
    """
    零售商品模块相关场景测试
    """

    def review(self, base_goods_id, review_type, status, review_status, verify_text):
        """
        审核
        :param base_goods_id:
        :param review_type:
        :param status:
        :param review_status:
        :param verify_text: 审核后校验的审核信息文本
        :return:
        """
        upgrade_goods_id = self.get_by_id(base_goods_id)

        # 审核通过
        data = {
            'method': 'dj.smartcarlife.api.upgradedGoods.submitReviewResult',
            'goodsId': upgrade_goods_id,
            'reviewType': review_type,
            'status': status,
            'reviewStatus': review_status,
            'sessionId': self.sid,
        }
        self.r = self.wpost(smartcarlife, data)
        self.common_assert()
        self.assert_equal('data', True)
        # 审核后，要等待一下再获取商品状态，否则可能获取的不是最新的状态
        sleep(1)
        # 再验证审核通过
        data = {
            'method': 'dj.api.basegoods.get.byId',
            'id': base_goods_id,
            'sessionId': self.sid,
        }
        self.r = self.wget(smartcarlife, data)
        self.common_assert()
        self.assert_equal('data.id', base_goods_id)
        self.assert_body_contains(verify_text)
        return

    def create_and_review(self):
        """
        创建商品并审核通过
        :return:
        """

        # 创建商品
        data = {
            'method': 'dj.api.basegoods.add',
            'merchantId': '44184606',
            'goodsCode': 'M220822102911411',
            'upgradeGoods[0].goodsCode': 'M220727112955451',
            'upgradeGoods[0].shopPrice': '1',
            'upgradeGoods[0].upgradePrice': '20',
            'upgradeGoods[0].incentiveType': '1',
            'upgradeGoods[0].shopMinPrice': '2',
            'upgradeGoods[0].warrantyPeriod': '5',
            'linkMerchants[0].merchantId': '44211229',
            'linkMerchants[0].yqMerchantId': '44211129',
            'sessionId': self.sid,
        }


        self.r = self.wpost(smartcarlife, data)
        self.common_assert()
        base_goods_id = self.extract('data.upgradeGoods[0].baseGoodsId')

        self.review(base_goods_id, '1', '0', '0', 'glsadmin通过了上架申请')

        return base_goods_id

    def delete(self, base_goods_id):
        """
        根据id删除商品
        :param base_goods_id:
        :return:
        """
        # 删除商品
        data = {
            'method': 'dj.smartcarlife.api.basegoods.delete',
            'baseGoodsId': base_goods_id,
            'sessionId': self.sid,
        }
        self.r = self.wpost(smartcarlife, data)
        self.common_assert()
        self.assert_equal('data.id', base_goods_id)
        return


    def get_by_id(self, base_goods_id):
        """
        根据id获取商品详情
        :param base_goods_id:
        :return:
        """
        data = {
            'method': 'dj.api.basegoods.get.byId',
            'id': base_goods_id,
            'sessionId': self.sid,
        }

        self.r = self.wget(smartcarlife, data)
        self.common_assert()
        self.assert_equal('data.id', base_goods_id)
        upgrade_goods_id = self.extract('data.upgradeGoodsList[0].id')

        return upgrade_goods_id

    def shelf_status_and_review(self, base_goods_id, shelf_status,review_type, status, review_status, verify_text):
        """
        上下架并审核
        :param base_goods_id:
        :param shelf_status:
        :param review_type:
        :param status:
        :param review_status:
        :param verify_text:
        :return:
        """
        data = {
            'method': 'dj.smartcarlife.api.basegoods.shelfStatus.update',
            'baseGoodsId': base_goods_id,
            'shelfStatus': shelf_status,
            'sessionId': self.sid,
        }
        self.r = self.wpost(smartcarlife, data)
        self.common_assert()
        self.assert_equal('data.id', base_goods_id)

        self.review(base_goods_id, review_type, status, review_status, verify_text)
        return

    def shelf_status_alone_and_review(self, base_goods_id, shelf_status,review_type, status, review_status, verify_text):
        """
        单独上下架并审核
        :param base_goods_id:
        :param shelf_status:
        :param review_type:
        :param status:
        :param review_status:
        :param verify_text:
        :return:
        """
        upgraded_goods_id = self.get_by_id(base_goods_id)
        # print(f'===> upgraded_goods_id is {upgraded_goods_id}')
        data = {
            'method': 'dj.smartcarlife.api.upgradedGoods.shelfStatus.update',
            'upgradedGoodsId': upgraded_goods_id,
            'shelfStatus': shelf_status,
            'sessionId': self.sid,
        }
        self.r = self.wpost(smartcarlife, data)
        self.common_assert()
        self.assert_equal('data', True)

        self.review(base_goods_id, review_type, status, review_status, verify_text)
        return

    @allure.title('产品管理—>零售商品->新增商品->成功')
    def test_create_material(self, admin_login):
        """
        产品管理—>零售商品->新增商品->成功,附加：产品管理—>零售商品->编辑->成功
        产品管理—>零售商品->编辑->产品成本->审核端（超管）审核通过->修改成功
        产品管理—>零售商品->编辑->产品成本->审核（超管）端审核驳回->修改失败
        产品管理—>零售商品->删除->成功
        :param admin_login:
        :return:
        """
        _, sid = admin_login
        self.sid = sid


        # 创建商品
        data = {
            'method': 'dj.api.basegoods.add',
            'merchantId': '44184606',
            'goodsCode': 'M220822102911411',
            'upgradeGoods[0].goodsCode': 'M220727112955451',
            'upgradeGoods[0].shopPrice': '1',
            'upgradeGoods[0].upgradePrice': '20',
            'upgradeGoods[0].incentiveType': '1',
            'upgradeGoods[0].shopMinPrice': '2',
            'upgradeGoods[0].warrantyPeriod': '5',
            'linkMerchants[0].merchantId': '44211229',
            'linkMerchants[0].yqMerchantId': '44211129',
            'sessionId': sid,
        }

        self.r = self.wpost(smartcarlife, data)
        self.common_assert()
        base_goods_id = self.extract('data.upgradeGoods[0].baseGoodsId')


        # 编辑商品
        upgrade_goods_id = self.get_by_id(base_goods_id)

        ## 未审核，修改关联的门店
        update_merchant_id = 44210991
        update_yqmerchant_id = 44211025
        data = {
            'method': 'dj.api.basegoods.update',
            'merchantId': '44184606',
            'goodsCode': 'M220822102911411',
            'retailPrice': '0',
            'shopPrice': '0',
            'upgradeGoods[0].goodsCode': 'M220727112955451',
            'upgradeGoods[0].shopPrice': '1',
            'upgradeGoods[0].upgradePrice': '20',
            'upgradeGoods[0].incentiveType': '1',
            'upgradeGoods[0].shopMinPrice': '2',
            'upgradeGoods[0].warrantyPeriod': '5',
            'upgradeGoods[0].id': upgrade_goods_id,
            'upgradeGoods[0].status': '0',
            'upgradeGoods[0].reviewStatus': '0',
            'id': base_goods_id,
            'linkMerchants[0].merchantId': update_merchant_id,
            'linkMerchants[0].yqMerchantId': update_yqmerchant_id,
            'sessionId': sid,
        }

        self.r = self.wpost(smartcarlife, data)
        self.common_assert()
        self.assert_equal('data.linkMerchants[0].merchantId', update_merchant_id)
        self.assert_equal('data.linkMerchants[0].yqMerchantId', update_yqmerchant_id)

        self.delete(base_goods_id)
        return


    @allure.title('产品管理—>零售商品->编辑->产品成本->审核端（超管）审核通过->修改成功')
    def test_edit_cost_price_passed(self, admin_login):
        """

        :param admin_login:
        :return:
        """
        _, sid = admin_login
        self.sid = sid

        # 先创建商品并审核通过使其上架
        base_goods_id = self.create_and_review()

        # 编辑产品成本
        upgrade_goods_id = self.get_by_id(base_goods_id)
        data = {
            'method': 'dj.api.basegoods.update',
            'merchantId': '44184606',
            'goodsCode': 'M220822102911411',
            'retailPrice': '0',
            'shopPrice': '0',
            'upgradeGoods[0].goodsCode': 'M220727112955451',
            'upgradeGoods[0].shopPrice': '3',
            'upgradeGoods[0].upgradePrice': '20',
            'upgradeGoods[0].incentiveType': '1',
            'upgradeGoods[0].shopMinPrice': '10',
            'upgradeGoods[0].warrantyPeriod': '5',
            'upgradeGoods[0].id': upgrade_goods_id,
            'upgradeGoods[0].status': '1',
            'upgradeGoods[0].reviewStatus': '1',
            'id': base_goods_id,
            'linkMerchants[0].merchantId': '44211229',
            'linkMerchants[0].yqMerchantId': '44211129',
            'sessionId': sid,
        }

        self.r = self.wpost(smartcarlife, data)
        self.common_assert()
        self.assert_equal('data.id', base_goods_id)

        # 审核: 修改产品成本
        self.review(base_goods_id, '1', '1', '0', 'glsadmin通过了成本修改申请')

        # 校验产品成本修改为新的值
        data = {
            'method': 'dj.api.basegoods.get.byId',
            'id': base_goods_id,
            'sessionId': self.sid,
        }

        self.r = self.wget(smartcarlife, data)
        self.common_assert()
        self.assert_equal('data.id', base_goods_id)
        # 商品成本重新设置为3，转换为浮点数
        new_shop_price = 3.0
        self.assert_equal('data.upgradeGoodsList[0].shopPrice', new_shop_price)

        # 下架并审核，然后删除商品
        self.shelf_status_and_review(base_goods_id, '0', '1', '1', '0', 'glsadmin通过了下架申请')
        self.delete(base_goods_id)
        return

    @allure.title('产品管理—>零售商品->编辑->产品成本->审核（超管）端审核驳回->修改失败')
    def test_edit_cost_price_failed(self, admin_login):
        """

        :param admin_login:
        :return:
        """
        _, sid = admin_login
        self.sid = sid

        # 先创建商品并审核通过使其上架
        base_goods_id = self.create_and_review()

        # 编辑产品成本
        upgrade_goods_id = self.get_by_id(base_goods_id)
        data = {
            'method': 'dj.api.basegoods.update',
            'merchantId': '44184606',
            'goodsCode': 'M220822102911411',
            'retailPrice': '0',
            'shopPrice': '0',
            'upgradeGoods[0].goodsCode': 'M220727112955451',
            'upgradeGoods[0].shopPrice': '3',
            'upgradeGoods[0].upgradePrice': '20',
            'upgradeGoods[0].incentiveType': '1',
            'upgradeGoods[0].shopMinPrice': '10',
            'upgradeGoods[0].warrantyPeriod': '5',
            'upgradeGoods[0].id': upgrade_goods_id,
            'upgradeGoods[0].status': '1',
            'upgradeGoods[0].reviewStatus': '1',
            'id': base_goods_id,
            'linkMerchants[0].merchantId': '44211229',
            'linkMerchants[0].yqMerchantId': '44211129',
            'sessionId': sid,
        }

        self.r = self.wpost(smartcarlife, data)
        self.common_assert()
        self.assert_equal('data.id', base_goods_id)

        # 审核: 修改产品成本
        self.review(base_goods_id, '2', '1', '0', 'glsadmin驳回了成本修改申请')

        # 校验产品成本还是原来的值
        data = {
            'method': 'dj.api.basegoods.get.byId',
            'id': base_goods_id,
            'sessionId': self.sid,
        }

        self.r = self.wget(smartcarlife, data)
        self.common_assert()
        self.assert_equal('data.id', base_goods_id)
        # 创建商品设置的成本是1，转换为浮点数
        orgin_shop_price = 1.0
        self.assert_equal('data.upgradeGoodsList[0].shopPrice', orgin_shop_price)

        # 下架并审核，然后删除商品
        self.shelf_status_and_review(base_goods_id, '0', '1', '1', '0', 'glsadmin通过了下架申请')
        self.delete(base_goods_id)
        return

    @allure.title('产品管理—>零售商品->上架->审核端（超管）审核驳回->上架失败(及相关场景)')
    def test_change_shelf_status(self, admin_login):
        """
        产品管理—>零售商品->上架->审核端（超管）审核驳回->上架失败
        产品管理—>零售商品->上架->审核端（超管）审核通过->上架成功
        产品管理—>零售商品->下架->审核端（超管）审核驳回->下架失败
        产品管理—>零售商品->下架->审核端（超管）审核通过->下架成功
        :param admin_login:
        :return:
        """
        _, sid = admin_login
        self.sid = sid

        # 上架->审核端（超管）审核驳回->上架失败
        base_goods_id = 250
        # '1' 代表上架  '0'代表下架
        shelf_status = '1'
        self.shelf_status_and_review(base_goods_id, shelf_status, '2', '0', '0', 'glsadmin驳回了上架申请')

        # 产品管理—>零售商品->上架->审核端（超管）审核通过->上架成功
        self.shelf_status_and_review(base_goods_id, shelf_status, '1', '0', '0', 'glsadmin通过了上架申请')

        # 产品管理— > 零售商品->下架->审核端（超管）审核驳回->下架失败
        shelf_status = '0'
        self.shelf_status_and_review(base_goods_id, shelf_status, '2', '1', '0', 'glsadmin驳回了下架申请')

        # 产品管理— > 零售商品->下架->审核端（超管）审核驳回->下架失败
        self.shelf_status_and_review(base_goods_id, shelf_status, '1', '1', '0', 'glsadmin通过了下架申请')
        return

    @allure.title('产品管理—>零售商品->单独上架->审核端（超管）审核驳回->单独上架失败(及相关场景)')
    def test_change_shelf_status_alone(self, admin_login):
        """
        产品管理—>零售商品->单独上架->审核端（超管）审核驳回->单独上架失败
        产品管理—>零售商品->单独上架->审核端（超管）审核通过->单独上架成功
        产品管理—>零售商品-单独下架->审核端（超管）审核驳回->单独下架失败
        产品管理—>零售商品->单独下架->审核端（超管）审核通过->单独下架成功
        :param admin_login:
        :return:
        """
        _, sid = admin_login
        self.sid = sid

        # 产品管理—>零售商品->单独上架->审核端（超管）审核驳回->单独上架失败
        base_goods_id = 250
        shelf_status = '1'
        self.shelf_status_alone_and_review(base_goods_id, shelf_status, '2', '0', '0', 'glsadmin驳回了上架申请')

        # 产品管理—>零售商品->单独上架->审核端（超管）审核通过->单独上架成功
        self.shelf_status_alone_and_review(base_goods_id, shelf_status, '1', '0', '0', 'glsadmin通过了上架申请')

        # 产品管理—>零售商品-单独下架->审核端（超管）审核驳回->单独下架失败
        shelf_status = '0'
        self.shelf_status_alone_and_review(base_goods_id, shelf_status, '2', '1', '0', 'glsadmin驳回了下架申请')

        # 产品管理—>零售商品->单独下架->审核端（超管）审核通过->单独下架成功
        self.shelf_status_alone_and_review(base_goods_id, shelf_status, '1', '1', '0', 'glsadmin通过了下架申请')
        return

    @allure.title('产品管理—>零售商品->导出->成功')
    def test_commodity_export(self, admin_login):
        """
        产品管理—>零售商品->导出->成功
        :param admin_login:
        :return:
        """
        _, sid = admin_login
        self.sid = sid

        # 获取文件uuid
        data = {
            'method': 'dj.api.common.async.exportExcel',
            'exportParam': '{"goodsName":"","goodsType":"","status":"","reviewStatus":"","brandMerchantCode":"","startDate":"","endDate":"","method":"dj.api.basegoods.export.async"}',
            'sessionId': sid,
        }
        self.r = self.wpost(smartcarlife, data)
        self.common_assert()
        self.assert_type('data', str)
        file_uuid = self.extract('data')

        # 轮训异步导出是否完成
        sleep(1.5)
        while True:
            sleep(0.5)
            data = {
                'method': 'dj.api.common.query.async.exportExcel',
                'fileUuidList[0]': file_uuid,
                'sessionId': sid,
            }
            self.r = self.wpost(smartcarlife, data)
            self.common_assert()
            file_info = self.extract('data[0]')
            if file_info['status'] == 1:
                break
        file_url = file_info['fileUrl']
        # 下载文件
        self.r = requests.get(file_url)
        assert self.r.status_code == 200, f'状态码错误，实际值{self.r.status_code}'
        self.assert_content_type('application/octet-stream')
        return

    ############################查询用例##################################

    def query(self, query_params=None):
        """
        商品查询接口
        :param query_params:
        :return:
        """
        data = {
            'method': 'dj.api.basegoods.page',
            'pageSize': '20',
            'currentPage': '1',
            'sessionId': self.sid,
        }
        if query_params is not None:
            data.update(**query_params)
        self.r = self.wget(smartcarlife, data)
        self.common_assert()
        return

    @allure.title('产品管理—>零售商品->(按商品名称)查询->成功')
    def test_commodity_query_1(self, admin_login):
        """
        产品管理—>零售商品->(按商品名称)查询->成功
        :param admin_login:
        :return:
        """
        _, sid = admin_login
        self.sid = sid

        #
        goods_name = '请别动'
        self.query({'goodsName': goods_name})
        self.assert_equal('data.total', 1)
        self.assert_in('data.list[0].goodsInfo.goodsName', goods_name)
        return

    @allure.title('产品管理—>零售商品->(按分类)查询->成功')
    def test_commodity_query_2(self, admin_login):
        """
        产品管理—>零售商品->(按分类)查询->成功
        :param admin_login:
        :return:
        """
        _, sid = admin_login
        self.sid = sid

        goods_type = 1
        query_param = {'goodsType': goods_type}
        self.query(query_param)
        self.assert_ge('data.total', 1)
        goods_list = self.extract('data.list')
        for goods in goods_list:
            type_list = [goods['goodsInfo']['goodsType']]
            for i in goods['upgradeGoodsList']:
                type_list.append(i['goodsInfo']['goodsType'])
            assert goods_type in type_list, f'查询结果的goodsType错误，不是{goods_type}'
        return

    @allure.title('产品管理—>零售商品->(按产品状态)查询->成功')
    def test_commodity_query_3(self, admin_login):
        """
        产品管理—>零售商品->(按产品状态)查询->成功
        :param admin_login:
        :return:
        """
        _, sid = admin_login
        self.sid = sid

        # 产品状态: 在售
        status = 1
        query_param = {'status': status}
        self.query(query_param)
        self.assert_ge('data.total', 1)
        goods_list = self.extract('data.list')
        # 部分在售，也算是在售，不做断言
        # for goods in goods_list:
        #     print(f"产品状态: {goods['status']}")
            # assert goods['status'] == status, f'状态错误,不是{status}'
        return





