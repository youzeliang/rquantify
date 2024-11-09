import json
import requests
import os, sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from utils import logger
from ding_engine import Message


class ConvertibleBonds:

    def __init__(self):
        self.message = Message()
        self.logger = logger.get_logger(log_dir=logger.LOG_FILE)

    def convertible_bonds(self):
        """
        convertible_bonds
        :return:
        """

        url = 'https://api.mrxiao.net/kzz'
        try:
            s = ''
            today_list = json.loads(requests.get(url).text)['today_start_kzz']
            if len(today_list) > 0:
                for i in range(0, len(today_list)):
                    s += '  ' + today_list[i]['SECURITY_NAME_ABBR']
                self.message.send_ding_message(s, True)
        except Exception as e:
            self.logger.error('convertible_bonds-err', e)
            self.message.send_ding_message('可转债接口异常', True)
