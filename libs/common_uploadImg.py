import requests
from libs.debugtalk import join_payload
import base64

#base64模块是用来做base64编码解码，常用于小型数据传输。编码后的数据是一个字符串，包括a-z，A-Z，/，+共64个字符

filname = 'D:\PyCharmProject\dj_api_test\image2.png'

com_url = 'http://dj.test.glsx.com.cn' #公共地址

def get_file_value(filename):
    """
    解析编码Excel文件，生成file参数的值
    :param filename: Excel文件路径
    :return:
    """
    # 以二进制格式读取文件内容
    with open(filename, 'rb') as f:
        content = f.read()

    content = base64.b64encode(content) #编码字符串
    #print(content)
    suffix_name = filename.split('.')[-1] #拿到文件后缀名
    #print(suffix_name)
    # file参数格式：文件名后缀 + @ + 文件内容进行base64编码后的字符串
    file_value = suffix_name+'@'+content.decode()
    #print(filname)
    return file_value


def pcPost_upload(path, data=None, file=None,**kwargs):
    """
    PC端 上传文件(图片等)专用
    该函数作用是把file与file_value 当做一个键值对加到join_payload里，使得计算sign值得时候，不会改变sign的值
    :return:
    """
    url =com_url+ path
    if data is not None:
        data = join_payload(data)

    #方法1
    #data.update(file = get_file_value(file)) #给公共的请求数据添加键值对file:file_value

    #方法2
    dic1 = {'file': get_file_value(file)}
    data.update(dic1)

    res = requests.post(url,data=data,**kwargs)
    # print(res.status_code)
    # print(res.headers)
    # print(res.text)

    return res


if __name__ == '__main__':

    #get_file_value('D:\PyCharmProject\dj_api_test\image.png')
    data = {
        'method': 'dj.api.common.uploadImg'
    }
    res = pcPost_upload('/rop-dj-smartcarlife/router',data=data,file=filname)
    print(res.json())
