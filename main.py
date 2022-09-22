import pytest
from time import strftime
from  os  import  system

def main1():
    """
    测试主函数入口
    :return:
    """
    times = strftime('%y%m%d %H%M%S') #获取时间格式
    report = f'report/report_{times}.html'
    # 运行testcases目录下以test_ 开头的用例
    #pytest.main(['-v',f'--html={report}','testcases/test_login.py'])  #登录用例
    #pytest.main(['testcases/test_order_select.py'])  # 订单查询用例
    pytest.main(['testcases'])

    system('allure generate reports/ --clean') #


if __name__ == '__main__':
    main1()