"""
@Description:
@Author: Lzc
@Time: 2022/9/1 15:30
@File: coupon_test.py
"""


import pytest
import allure
from lib.request import HttpRequest
from random import randint,choice
import requests
from time import sleep
from pprint import pprint
from lib.router import smartcarlife


@allure.feature('产品管理')
@allure.story('发券宝')
@pytest.mark.dj_admin
@pytest.mark.dj_admin_product
class TestCoupon(HttpRequest):
    """
    零售商品模块相关场景测试
    """

    def coupon_list(self, query_params = None):
        """
        查询优惠券
        :param query_params: 查询参数
        :return:
        """
        data = {
            'method': 'dj.api.life.merchant.coupon.list',
            'pageSize': '20',
            'currentPage': '1',
            'sessionId': self.sid,
        }
        if query_params is not None:
            data.update(**query_params)

        self.r = self.wget(smartcarlife, data)
        self.common_assert()

        return

    def customer_coupon_list(self, query_params = None):
        """
        查询优惠券领用明细
        :param query_params: 查询参数
        :return:
        """
        data = {
            'method': 'dj.api.life.customer.coupon.list',
            'pageSize': '20',
            'currentPage': '1',
            'sessionId': self.sid,
        }
        if query_params is not None:
            data.update(**query_params)

        self.r = self.wget(smartcarlife, data)
        self.common_assert()

        return


    @allure.title('产品管理—>发劵宝->店面列表-新增->编辑->查询->删除->成功')
    def test_main_flow_1(self, admin_login):
        """
        主流程测试
        :return:
        """
        _, self.sid = admin_login

        # ===> 创建 <===
        coupon_name = '宾利5元代金券'
        data = {
            'method': 'dj.api.life.coupon.info.add',
            'couponName': coupon_name,
            'couponType': '1',
            'couponTypeName': '太阳膜',
            'chargeFlag': 'N',
            'remark': '出示此券，立减五元',
            'merchantCouponDTOList[0].yqMerchantId': '44211129',
            'merchantCouponDTOList[0].yqMerchantName': '账户同步测试园区店',
            'merchantCouponDTOList[0].merchantId': '44211132',
            'merchantCouponDTOList[0].merchantName': '账户同步测试4S店',
            'merchantCouponDTOList[0].channelType': '2',
            'merchantCouponDTOList[0].amount': '999',
            'createdBy': '广联嘀加平台超级管理员',
            'sessionId': self.sid,
        }
        self.r = self.wpost(smartcarlife, data)
        self.common_assert()
        self.assert_equal('data.couponName', coupon_name)
        coupon_id = self.extract('data.id')
        merchant_coupon_id = self.extract('data.merchantCouponDTOList[0].id')

        # 查询验证创建成功(顺便测试查询接口)
        self.coupon_list({'couponName': coupon_name})
        self.assert_equal('data.total', 1)

        # ===> 编辑 <===
        coupon_info = self.extract('data.list[0]')
        new_coupon_name = '新' + coupon_info['couponName']
        data = {
            'id': coupon_info['id'],
            'couponId': coupon_info['couponId'],
            'couponName': new_coupon_name,
            'merchantCouponCode': coupon_info['merchantCouponCode'],
            'remark': coupon_info['remark'],
            'enabledFlag': coupon_info['enabledFlag'],
            'yqMerchantId': coupon_info['yqMerchantId'],
            'yqMerchantName': coupon_info['yqMerchantName'],
            'merchantId': coupon_info['merchantId'],
            'merchantName': coupon_info['merchantName'],
            'channelType': coupon_info['channelType'],
            'amount': coupon_info['amount'],
            'usedAmount': coupon_info['usedAmount'],
            'getAmount': coupon_info['getAmount'],
            'createdBy': '广联嘀加平台超级管理员',
            'createdDate': coupon_info['createdDate'],
            'updatedBy': coupon_info['updatedBy'],
            'updatedDate': coupon_info['updatedDate'],

            'couponInfo.couponName': coupon_info['couponInfo']['couponName'],
            'couponInfo.couponType': coupon_info['couponInfo']['couponType'],
            'couponInfo.couponTypeName': coupon_info['couponInfo']['couponTypeName'],
            'couponInfo.chargeFlag': coupon_info['couponInfo']['chargeFlag'],
            'remainAmount': coupon_info['remainAmount'],

            'undefined': '1',
            'chargeFlag': coupon_info['couponInfo']['chargeFlag'],
            'couponType': coupon_info['couponInfo']['couponType'],
            'couponTypeName': coupon_info['couponInfo']['couponTypeName'],

            'method': 'dj.api.life.merchant.coupon.update',
            'sessionId': self.sid,
        }

        self.r = self.wpost(smartcarlife, data)
        self.common_assert()
        self.assert_equal('data.couponName', new_coupon_name)

        # 查询验证编辑优惠券名称成功(顺便测试查询接口)
        self.coupon_list({'couponName': new_coupon_name})
        self.assert_equal('data.total', 1)

        # ===> 删除 <===
        data = {
            'method': 'dj.api.life.merchant.coupon.delete',
            'id': merchant_coupon_id,
            'sessionId': self.sid,
        }
        self.r = self.wget(smartcarlife, data)
        self.common_assert()
        self.assert_equal('data', True)

        # 查询验证删除成功(顺便测试查询接口)
        self.coupon_list({'couponName': new_coupon_name})
        self.assert_equal('data.total', 0)

    @allure.title('产品管理—>发劵宝->店面列表-新增->查询->导出->停用->删除->成功')
    def test_main_flow_2(self, admin_login):
        """
        主流程测试
        :return:
        """
        _, self.sid = admin_login

        # ===> 创建 <===
        coupon_name = '五菱宏光5元代金券'
        data = {
            'method': 'dj.api.life.coupon.info.add',
            'couponName': coupon_name,
            'couponType': '1',
            'couponTypeName': '太阳膜',
            'chargeFlag': 'N',
            'remark': '出示此券，立减五元',
            'merchantCouponDTOList[0].yqMerchantId': '44211129',
            'merchantCouponDTOList[0].yqMerchantName': '账户同步测试园区店',
            'merchantCouponDTOList[0].merchantId': '44211132',
            'merchantCouponDTOList[0].merchantName': '账户同步测试4S店',
            'merchantCouponDTOList[0].channelType': '2',
            'merchantCouponDTOList[0].amount': '999',
            'createdBy': '广联嘀加平台超级管理员',
            'sessionId': self.sid,
        }
        self.r = self.wpost(smartcarlife, data)
        self.common_assert()
        self.assert_equal('data.couponName', coupon_name)
        coupon_id = self.extract('data.id')
        merchant_coupon_id = self.extract('data.merchantCouponDTOList[0].id')

        # 查询验证创建成功(顺便测试查询接口)
        self.coupon_list({'couponName': coupon_name})
        self.assert_equal('data.total', 1)

        # ===> 导出 <===
        export_param = '{"couponName":"%s","merchantName":"","currentPage":1,"method":"dj.api.life.merchant.coupon.exportExcel.async"}'%coupon_name
        self.export_excel(export_param, 'application/octet-stream')

        # ===> 停用 <===
        data = {
            'method': 'dj.api.life.merchant.coupon.update',
            'id': merchant_coupon_id,
            'enabledFlag': 'N',
            'sessionId': self.sid,
        }
        self.r = self.wpost(smartcarlife, data)
        self.common_assert()
        self.assert_equal('data.id', merchant_coupon_id)
        self.assert_equal('data.enabledFlag', 'N')


        # ===> 删除 <===
        data = {
            'method': 'dj.api.life.merchant.coupon.delete',
            'id': merchant_coupon_id,
            'sessionId': self.sid,
        }
        self.r = self.wget(smartcarlife, data)
        self.common_assert()
        self.assert_equal('data', True)

        # 查询验证删除成功(顺便测试查询接口)
        self.coupon_list({'couponName': coupon_name})
        self.assert_equal('data.total', 0)
        return

    @allure.title('产品管理—>发劵宝->店面列表-查询->成功')
    def test_query_by_merchant(self, admin_login):
        """

        :return:
        """
        _, self.sid = admin_login
        merchant_name = '小苏门店'
        self.coupon_list({'merchantName': merchant_name})
        coupon_list = self.extract('data.list')
        for coupon in coupon_list:
            assert merchant_name in coupon['merchantName']

        return

    @allure.title('产品管理—>发劵宝->(按门店名称查询)领用明细-查询')
    def test_take_detail_query_1(self, admin_login):
        """

        :return:
        """
        _, self.sid = admin_login

        merchant_name = '小苏门店'
        self.customer_coupon_list({'merchantName': merchant_name})
        self.assert_ge('data.total', 1)
        coupon_list = self.extract('data.list')
        for coupon in coupon_list:
            assert merchant_name in coupon['merchantCoupon']['merchantName']
        return

    @allure.title('产品管理—>发劵宝->(按礼券名称查询)领用明细-查询')
    def test_take_detail_query_2(self, admin_login):
        """

        :return:
        """
        _, self.sid = admin_login

        coupon_name = '麦礼券'
        self.customer_coupon_list({'couponName': coupon_name})
        self.assert_ge('data.total', 1)
        coupon_list = self.extract('data.list')
        for coupon in coupon_list:
            assert coupon_name in coupon['couponName']
        return


