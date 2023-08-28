import os

import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import base64
import hmac
import urllib.parse
import requests
from utils import logger
from utils.global_vars import *


class Message:
    def __init__(self, secret=config['DingTalk'].get('Secret'), webhook=config['DingTalk'].get('Webhook')):
        """"
            send the message to DingTalk Group
            see the detail https://open.dingtalk.com/document/robots/robot-overview
        """

        self.default_logger = logger.Logger().logger
        self.secret = secret
        self.webhook = webhook

    def sign(self):
        timestamp = str(round(time.time() * 1000))
        secret = self.secret
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign_res = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return timestamp, sign_res

    def send_ding_message(self, text_info, flag):
        webhook = self.webhook
        header = {
            "Content-Type": "application/json",
            "Charset": "UTF-8"
        }
        text = text_info
        message = {
            "msgtype": "text",
            "text": {
                "content": text
            },
            "at": {
                "isAtAll": flag
            }
        }
        timestamp, sign_res = self.sign()
        webhook += "&timestamp=" + timestamp + "&sign=" + sign_res
        info = requests.post(url=webhook, data=json.dumps(message), headers=header)
        if json.loads(info.text).get('errcode') != 0:
            self.default_logger.error('send DingTalk Group message err.%s', json.loads(info.text))


if __name__ == '__main__':
    m = Message()
    m.send_ding_message('fdfs', True)
