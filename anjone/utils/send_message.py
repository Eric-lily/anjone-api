# -*- coding: utf-8 -*-
import random

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
# 导入对应产品模块的client models。
from tencentcloud.sms.v20210111 import sms_client, models

# 导入可选配置类
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile

from anjone.utils.cache import cache

secretId = "AKIDay5wVnnW2GCqDI5bpmSrzqPhiV1FCrFM"
secretKey = "tVpthEYbMpjRt4zf7JH2e18za2MRN7an"
endpoint = "sms.tencentcloudapi.com"
reqTimeout = 30
reqMethod = "POST"

SmsSdkAppId = "1400673483"
SignName = "0xffff个人网站"
TemplateId = "1560921"


def get_random_str():
    alphabet = '1234567890'
    return random.sample(alphabet, 4)


# 发送短信的静态类
class Message(object):

    @staticmethod
    def send_message(phone):
        try:
            # 实例化一个认证对象，入参需要传入腾讯云账户密钥对secretId，secretKey。
            cred = credential.Credential(secretId, secretKey)
            # 实例化一个http选项，可选的，没有特殊需求可以跳过。
            httpProfile = HttpProfile()
            httpProfile.reqMethod = reqMethod
            httpProfile.reqTimeout = reqTimeout
            httpProfile.endpoint = endpoint
            # 实例化一个客户端配置对象，可以指定超时时间等配置
            clientProfile = ClientProfile()
            clientProfile.signMethod = "TC3-HMAC-SHA256"  # 指定签名算法
            clientProfile.language = "zh-hans"
            clientProfile.language = "en-US"
            # 实例化要请求产品(以sms为例)的client对象
            # 第二个参数是地域信息，可以直接填写字符串ap-guangzhou，支持的地域列表参考 https://cloud.tencent.com/document/api/382/52071#.E5.9C.B0.E5.9F.9F.E5.88.97.E8.A1.A8
            client = sms_client.SmsClient(cred, "ap-guangzhou", clientProfile)
            # 实例化请求对象
            req = models.SendSmsRequest()
            req.SmsSdkAppId = SmsSdkAppId
            req.SignName = SignName
            req.TemplateId = TemplateId
            # 手机号
            req.PhoneNumberSet = ['+86'+phone]
            # 验证码
            code = ''.join(get_random_str())
            req.TemplateParamSet = [code]
            # 缓存
            # todo 设置过期时间
            cache.set(phone, code)
            # 获取响应
            resp = client.SendSms(req)
            print(resp.to_json_string(indent=2))
        except TencentCloudSDKException as err:
            raise err


if __name__ == '__main__':
    Message.send_message('18373687376')
