import csv
import os
import sys
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from pathlib import Path

from trading_engine import FutuTrade

# Get the current directory where the script is located
current_directory = Path(__file__).parent

# Create the log directory at the same level as the "engines" directory
download_directory = current_directory / "../downloads"
download_directory.mkdir(parents=True, exist_ok=True)

from utils.global_vars import *
from utils import logger

import datetime
from datetime import date


class Data:
    def __init__(self):
        """
            Futu download data
        """
        self.config = config
        self.port = int(self.config['FutuOpenD.Config'].get('Port'))
        self.host = str(self.config['FutuOpenD.Config'].get('Host'))
        self.quote_ctx = OpenQuoteContext(host=self.host,
                                          port=self.port)
        self.trade_ctx = OpenSecTradeContext(filter_trdmarket=TrdMarket.HK,
                                             host=self.host,
                                             security_firm=SecurityFirm.FUTUSECURITIES)
        self.logger = logger.get_logger(log_dir=logger.LOG_FILE)
        self.trading = FutuTrade(self.quote_ctx, self.trade_ctx)


    def __del__(self):
        pass

    def down_single_min_data(self, stock_code, index, data_path):
        csv_name = stock_code.split(".")[-1] + '_' + index_k[index]
        yesterday = str(datetime.date.today() + datetime.timedelta(-1))
        path = data_path
        if platform.system().lower() != 'linux':
            path = '../downloads/'
        if os.path.isfile(path + csv_name + '.csv'):
            last_line = ''
            with open(path + csv_name + '.csv') as f_l:
                lines = f_l.readlines()
                if len(lines) > 1:
                    last_line = lines[-1]
                else:
                    os.remove(path + csv_name + '.csv')
            if last_line != '':
                f = open(path + csv_name + '.csv', 'a+')
                writer = csv.writer(f)
                res = self.trading.get_history_kline(stock_code, index_type[index], start_date=yesterday,
                                                     end_date=yesterday)
                if len(res) > 0:
                    for x in range(0, len(res)):
                        data_list_temp = [
                            [res['open'][x], res['close'][x], res['high'][x], res['low'][x], res['volume'][x],
                             res['turnover'][x], res['change_rate'][x], res['last_close'][x], res['time_key'][x]]]
                        writer.writerows(data_list_temp)

        else:
            pass_day = str(date.today().year - 2) + '-' + str(date.today().month) + '-' + str(
                date.today().day)
            if index == 6:
                pass_day = str(date.today().year - 10) + '-' + str(date.today().month) + '-' + str(
                    date.today().day)
            res = self.trading.get_history_kline(stock_code, index_type[index], start_date=pass_day,
                                                 end_date=yesterday)
            f = open(path + csv_name + '.csv', 'w')
            writer = csv.writer(f)
            writer.writerows(
                [['open', 'close', 'high', 'low', 'volume', 'turnover', 'change_rate', 'last_close', 'time_key']])
            if len(res) > 0:
                for x in range(0, len(res)):
                    data_list_temp = [
                        [res['open'][x], res['close'][x], res['high'][x], res['low'][x], res['volume'][x],
                         res['turnover'][x], res['change_rate'][x], res['last_close'][x], res['time_key'][x]]]
                    writer.writerows(data_list_temp)

    def get_us_quoty_code_list(self, page):
        url = 'https://www.futunn.com/quote-api/quote-v2/get-stock-list'

        params = {
            'marketType': 2,
            'plateType': 1,
            'rankType': 5,
            'page': page,
            'pageSize': 50
        }

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'cookie': futu_api[str(page)]['cookie'],
            'dnt': '1',
            'futu-x-csrf-token': 'wPN0j4mwm6Uu4Pp-kJYwkngV',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'quote-token': futu_api[str(page)]['quote-token'],
            'referer': 'https://www.futunn.com/quote/us/stock-list/all-us-stocks/top-turnover',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }

        response = requests.get(url, headers=headers, params=params)

        return json.loads(response.text)


if __name__ == '__main__':
    data = Data()
    data.down_single_min_data('HK.800000', 0, download_directory)
