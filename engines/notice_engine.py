import os, sys
import socket
import requests
import time
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from utils import logger

from engines.init_engine import Init


class Notice:

    def __init__(self):
        self.init = Init()
        self.logger = logger.get_logger(log_dir=logger.LOG_FILE)

    def check_port(self):
        """
        Check if the Futu port is started up correctly.

        :return:
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.init.host, self.init.port))
            s.shutdown(2)
            self.logger.info("port is open")
            return True
        except Exception as e:
            logger.get_logger(log_dir=logger.ERROR_LOG_FILE).error(e)
            return False

    def economic_data(self):
        current_date = datetime.datetime.now()
        formatted_date = current_date.strftime('%m/%d')
        url = f'https://cdn-rili.jin10.com/web_data/{current_date.year}/daily/{formatted_date}/economics.json?t=1693451525225'
        response = requests.get(url)
        data = response.json()
        for i in data:
            if i['country'] in ['中国', '美国'] or int(i['star']) >= 3:
                continue
            ignore = [
                '天然气', '芝加哥'
            ]

            flag = False
            for x in ignore:
                if x in str(i['name']):
                    flag = True
                    break
            if flag:
                continue

            current_timestamp = int(time.time())
            if i['pub_time_unix'] > current_timestamp:
                continue

            s = i['country'] + ' ' + i['name'] + ' ' + '  前值:' + str(i['previous']) + ' ' + '  预期值: ' + str(
                i['consensus']) + '  实际值: ' + str(i['actual']) + '  ' + str(i['star']) + '星'

            return s
