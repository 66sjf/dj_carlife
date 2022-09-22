import  requests
from libs import  debugtalk
def login():
    """
    登录逻辑,封装为公共函数，返回sessionID，方便后续接口调用
    """
    url1 = 'http://dj.test.glsx.com.cn/rop-dj-smartcarlife/router'
    params1 = {
        'userName': 'aa123456',
        'password': '8a6f2805b4515ac12058e79e66539be9',
        'method':'dj.api.user.login'
    }
    res1 = requests.get(url=url1,params=debugtalk.join_payload(params1)) #返回响应对象
    #print(res1.json())
    #print(res1.json()['data']['sessionId'])#拿到sessionId，方便后面下游接口使用
    return  res1.json()['data']['sessionId']

if __name__ == '__main__':
    print(login())