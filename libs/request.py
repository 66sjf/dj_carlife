import functools
from json import decoder, dumps
from typing import Any
import requests
from requests.models import Response
from lib.init_params import join_payload
import jmespath
from pprint import pprint
import base64
from time import sleep


# 精品升级小程序url前缀
base_url = 'https://dj.test.glsx.com.cn'
# 智享车生活(D+) 后台url前缀
pc_url = 'http://dj.test.glsx.com.cn'


def get_file_value(filename):
    """
    解析编码Excel文件，生成file参数的值
    :param filename: Excel文件路径
    :return:
    """
    # 以二进制格式读取文件内容
    with open(filename, 'rb') as f:
        content = f.read()

    content = base64.b64encode(content)
    suffix_name = filename.split('.')[-1]
    # file参数格式：文件名后缀 + @ + 文件内容进行base64编码后的字符串
    file_value = suffix_name + '@' + content.decode()
    return file_value


class HttpRequest(object):
    """
    http请求封装
    """


    def get(self, path, params=None, **kwargs):
        url = base_url + path
        if params is not None:
            params = join_payload(params, client_type='wechat')
        return requests.get(url, params=params, **kwargs)
        # return requests.get(url, params=params, **kwargs,  verify=False, proxies={'https':'http://127.0.0.1:8888'})


    def post(self, path, data=None, json=None, **kwargs):
        url = base_url + path
        if data is not None:
            data = join_payload(data, client_type='wechat')
        return requests.post(url, data=data, json=json, **kwargs)
        # return requests.post(url, data=data, json=json, **kwargs, verify=False, proxies={'https':'http://127.0.0.1:8888'})

    def wget(self, path, params=None, **kwargs):
        """
        PC端GET请求
        :param path:
        :param params:
        :param kwargs:
        :return:
        """
        url = pc_url + path
        if params is not None:
            params = join_payload(params)
        return requests.get(url, params=params, **kwargs)
        # return requests.get(url, params=params, **kwargs,  verify=False, proxies={'http':'http://127.0.0.1:8888'})


    def wpost(self, path, data=None, json=None, **kwargs):
        """
        PC端POST请求
        :param path:
        :param data:
        :param json:
        :param kwargs:
        :return:
        """
        url = pc_url + path
        if data is not None:
            data = join_payload(data)

        # pprint(data)
        return requests.post(url, data=data, json=json, **kwargs)
        # return requests.post(url, data=data, json=json, **kwargs, verify=False, proxies={'http':'http://127.0.0.1:8888', 'https':'http://127.0.0.1:8888'})

    @staticmethod
    def post_upload(path, data=None, json=None, file=None, **kwargs):
        """
        精品升级小程序端POST请求,上传文件(图片等)专用
        :param path:
        :param data:
        :param json:
        :param file:
        :param kwargs:
        :return:
        """
        url = pc_url + path
        if data is not None:
            data = join_payload(data, client_type='wechat')

        data.update(file=get_file_value(file))
        return requests.post(url, data=data, json=json, **kwargs)
        # return requests.post(url, data=data, json=json, **kwargs,  verify=False, proxies={'https':'http://127.0.0.1:8888'})

    @staticmethod
    def wpost_upload(path, data=None, json=None, file=None, **kwargs):
        """
        PC端POST请求,上传文件(图片等)专用
        :param path:
        :param data:
        :param json:
        :param file:
        :param kwargs:
        :return:
        """
        url = pc_url + path
        if data is not None:
            data = join_payload(data)

        data.update(file=get_file_value(file))
        return requests.post(url, data=data, json=json, **kwargs)

    def export_excel(self, export_param, expected_content_type):
        """
        异步导出Excel文件公共函数
        :param export_param: 导出参数，用于method: dj.api.common.async.exportExcel
        :param expected_content_type: 预期导出文件的媒体类型
        :return:
        """
        # 获取文件uuid
        data = {
            'method': 'dj.api.common.async.exportExcel',
            'exportParam': export_param,
            'sessionId': self.sid,
        }
        self.r = self.wpost('/rop-dj-smartcarlife/router', data)
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
                'sessionId': self.sid,
            }
            self.r = self.wpost('/rop-dj-smartcarlife/router', data)
            self.common_assert()
            file_info = self.extract('data[0]')
            if file_info['status'] == 1:
                break
        file_url = file_info['fileUrl']
        # print(f'文件路径: {file_url}')

        # 下载文件
        self.r = requests.get(file_url)
        assert self.r.status_code == 200, f'状态码错误，实际值{self.r.status_code}'
        self.assert_content_type(expected_content_type)
        return

    def extract(self, path: str):
        """
        从响应中提取指定字段的值(注意：字段的值不能为空，否则会被认为jmespath路径错误)
        :param path:
        :return:
        """
        data = self.r.json()
        ret = jmespath.search(path, data)
        if ret is None:
            raise ValueError('jmespath路径错误')
        return ret

    def common_assert(self):
        """
        通用断言，断言HTTP状态码，响应体的code和message字段
        :return: None
        """
        resp = self.r
        status_code = resp.status_code
        body = resp.json()
        code = body.get('code')
        msg = body.get('message')
        assert status_code == 200, f'状态码错误，实际值是{status_code}\n{body}'
        assert code == '0', f'code字段错误，实际值是{code}\n{body}'
        assert msg == '调用服务成功!', f'message字段错误，实际值是{msg}'

    def assert_body_contains(self, text: str):
        """
        断言响应体中包含指定的文本
        :param resp:
        :param text:
        :return:
        """

        assert text in self.r.text, f'response body does not contain {text}'

    def assert_body_not_contains(self, text: str):
        """
        断言响应体中包含指定的文本
        :param resp:
        :param text:
        :return:
        """

        assert text not in self.r.text, f'response body contains {text}'

    def assert_equal(self, path, value):
        """
        断言响应体中json字段的值
        :param path:
        :param value:
        :return:
        """
        data = self.r.json()
        ret = jmespath.search(path, data)
        assert value == ret, f'assert {value} == {ret}'

    def assert_gt(self, path, value):
        """
        断言响应体中json字段的值
        :param path:
        :param value:
        :return:
        """
        data = self.r.json()
        ret = jmespath.search(path, data)
        assert ret > value, f'assert {ret} > {value}'

    def assert_ge(self, path, value):
        """
        断言响应体中json字段的值
        :param path:
        :param value:
        :return:
        """
        data = self.r.json()
        ret = jmespath.search(path, data)
        assert ret >= value, f'assert {ret} >= {value}'

    def assert_lt(self, path, value):
        """
        断言响应体中json字段的值
        :param path:
        :param value:
        :return:
        """
        data = self.r.json()
        ret = jmespath.search(path, data)
        assert ret < value, f'assert {ret} < {value}'

    def assert_le(self, path, value):
        """
        断言响应体中json字段的值
        :param path:
        :param value:
        :return:
        """
        data = self.r.json()
        ret = jmespath.search(path, data)
        assert ret <= value, f'assert {ret} <= {value}'


    def assert_in(self, path, value):
        """
        断言响应体中json字段的值
        :param path:
        :param value:
        :return:
        """
        data = self.r.json()
        ret = jmespath.search(path, data)
        assert value in ret, f'assert {value} in {ret}'

    def assert_type(self, path, target_type):
        """
        断言响应体中json字段的值
        :param path:
        :param target_type:
        :return:
        """
        data = self.r.json()
        ret = jmespath.search(path, data)
        assert isinstance(ret, target_type), f'assert {ret}不是{target_type}类型'

    def assert_content_type(self, expected_content_type):
        """
        断言响应体中json字段的值
        :param expected_content_type:
        :return:
        """
        value = self.r.headers.get('Content-Type')
        msg = f'响应头中Content-Type不是{expected_content_type}, 实际值: {value}'
        assert expected_content_type in value, msg


def check_response(describe: str = '',
                   status_code: int = 200,
                   ret: Any = None,
                   check: Any = None,
                   debug: bool = False):
    """
    检查接口响应数据
    :param describe: 封装方法描述
    :param status_code: 判断接口返回的HTTP状态码，默认200
    :param ret: 提取接口返回的字段
    :param check: 检查接口返回的字段
    :param debug: 开启debug，打印更多信息
    :return:
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__

            # 执行函数
            r = func(*args, **kwargs)

            assert r.status_code == status_code, f'{func_name}请求时, 状态码不等于预期值: {r.status_code} != {status_code}'

            try:
                r.json()
            except decoder.JSONDecodeError:

                raise Exception(
                    f'Execute {func_name} - {describe} failed: Not in JSON format'
                )


            if hasattr(check, '__call__'):
                if check():
                    for expr, value in check().items():
                        data = jmespath.search(expr, r.json())
                        # data = utils_jmespath(expr, r.json())
                        assert data == value, f'{func_name} 请求时, 响应体不等于预期值:{data} != {value}'
            else:
                if check is not None:
                    for expr, value in check.items():
                        data = jmespath.search(expr, r.json())
                        # data = utils_jmespath(expr, r.json())
                        assert data == value, f'{func_name} 请求时, 响应体不等于预期值:{data} != {value}\n{r.json()}'

            if hasattr(ret, '__call__'):
                if ret():
                    # data = utils_jmespath(ret(), r.json())
                    data = jmespath.search(ret(), r.json())
                else:
                    return r.json()

                return data
            else:
                if ret is not None:
                    # data = utils_jmespath(ret, r.json())
                    data = jmespath.search(ret, r.json())
                    return data
                else:
                    return r.json()

        return wrapper

    return decorator
