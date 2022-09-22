import requests
from libs.debugtalk import join_payload

com_url = 'http://dj.test.glsx.com.cn' #公共地址
class HttpRequest():
    def dj_post(path,data):
        """
        post请求进行封装
        :param path:  请求路径
        :param data:  请求参数
        :return:
        """
        url = com_url +path
        res = requests.post(url,data=join_payload(data))

        # 进行登录状态码断言
        assert res.status_code == 200, '预期状态码与实际不一致'

        # 进行code断言,预期结果与实际结果进行对比
        assert res.json()['code'] == '0', '预期code的值与实际值不一致'

        # 进行message断言，预期结果与实际结果进行对比
        assert res.json()['message'] == '调用服务成功!', '预期message的值与实际值不一致'

        return  res


    def dj_get(path,params):
        """
        get请求进行封装
        :param path:  请求路径
        :param params:  请求参数
        :return:
        """
        url =com_url+path
        res = requests.get(url,params=join_payload(params))

        # 进行登录状态码断言
        print(res.status_code)
        assert res.status_code == 200, '预期状态码与实际不一致'

        # 进行code断言,预期结果与实际结果进行对比
        assert res.json()['code'] == '0', '预期code的值与实际值不一致'

        # 进行message断言，预期结果与实际结果进行对比
        assert res.json()['message'] == '调用服务成功!', '预期message的值与实际值不一致'

        return res



