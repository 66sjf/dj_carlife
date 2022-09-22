import hashlib
import os
from datetime import datetime
from typing import Dict


def get_sign(payload: Dict) -> str:
    """获取签名sign并返回

    :param payload: 请求参数，键值对字典
    :type payload: Dict
    """
    payload_str = sorted_payload_to_str(payload)
    sign = payload_str_sha1(payload_str)
    return sign


def sorted_payload_to_str(payload: Dict) -> str:
    """请求参数按照字母先后顺序排序，
    参数名和参数值连接后，得到拼装字符串

    :param payload: 请求参数，键值对字典
    :type payload: Dict
    :return: 返回拼接后的字符串
    :rtype: str
    """
    key_value_str = ''
    #sorted 可以对所有可迭代的对象进行排序操作
    for key in sorted(payload):
        key_value_str += (key + str(payload[key]))

    return key_value_str


def payload_str_sha1(payload_str: str) -> str:
    """将secret拼接到参数字符串头、尾进行SHA1加密后返回

    :param payload_str: 排序好的参数字符串
    :type payload_str: str
    :return: 加密后数据
    :rtype: str
    """
    # 读取.env文件中秘钥
    # secret = os.environ["SECRET"]
    secret = 'c24619ed7fef02a0ae16328146bca5f97cc6493957a2137b'

    # 待加密字符串
    unencrypted_str = secret + payload_str + secret

    # 使用sha1算法加密，转换为大写，返回最终的密钥
    sha1_obj = hashlib.sha1()
    sha1_obj.update(unencrypted_str.encode('utf-8'))
    encrypted_str = sha1_obj.hexdigest().upper()

    return encrypted_str


def join_payload(payload: Dict) -> Dict:
    """获取sign，添加到到请求body并返回

    :param payload: 请求参数
    :type payload: Dict
    :return: 返回更新后字典
    :rtype: Dict
    """
    fixed_params = {
        "v": "1.0.0",
        "format": "json",
        "locale": "zh_CN",
        "appKey": "48e5e13229b82c1b4e6e8c96151f0637",
        'timestamp': get_now_time()
    }
    payload.update(fixed_params)
    # payload.update({"sign": get_sign(payload)})
    payload.update({"sign": get_sign(payload)})

    return payload


def get_encrypt_password() -> str:
    """原密码md5加密后返回

    :return: 返回加密密码
    :rtype: str
    """
    raw_passwd = os.environ["PASSWORD"]  # 读取.env中密码
    md5_obj = hashlib.md5()
    md5_obj.update(raw_passwd.encode(encoding='utf-8'))

    return md5_obj.hexdigest()


def get_now_time() -> int:
    """获取当前时间，并返回时间戳

    :return: 当前时间戳
    :rtype: int
    """
    timestamp = int(datetime.now().timestamp() * 1000)

    return timestamp



def get_dict_info(params: dict, key: str):
    """

    :param params:
    :param key:
    :return:
    """
    return params.get(key)




