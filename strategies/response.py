from futu import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import requests

t = time.localtime()
d = t.tm_mday
h = t.tm_hour
m = t.tm_min

import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


class OResponse:

    def __init__(self, text_info, webhook_url, sender_id, s_logger):
        self.webhook_url = webhook_url
        self.sender_id = sender_id
        self.default_logger = s_logger
        self.text_info = text_info

    def send_msg(self, userid, message, webhook_url):
        data = {
            "msgtype": "text",
            "text": {
                "content": message
            },
            "at": {
                "atUserIds": [
                    userid
                ]
            }
        }
        if message == '':
            self.default_logger.info('message没有数据')
            return
        if platform.system() == 'Darwin':
            print(message)
            return
        req = requests.post(webhook_url, json=data)
        if req.status_code != 200:
            self.default_logger.error(req.text)

    def handle_text_info(self):
        pass
    # todo handle self.text_info


if __name__ == '__main__':
    pass
