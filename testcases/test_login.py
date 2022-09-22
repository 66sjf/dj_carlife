import  requests
from libs import  debugtalk
import  pytest
import allure
from  libs.common_request import HttpRequest


@allure.feature('登录')
@pytest.mark.dj_pc_login
class TestLogin():
    @allure.title('登录成功')
    def test_login_success(self):
        """
        登录成功
        :return:
        """
        with allure.step('步骤1：调用请求，返回响应数据'):
            params = {
                'userName': 'aa123456',
                'password': '8a6f2805b4515ac12058e79e66539be9',
                'method': 'dj.api.user.login'
            }
            res = HttpRequest.dj_get('/rop-dj-smartcarlife/router',params)

        return res






