import curses
import os, sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from utils.global_vars import *
from trading_engine import FutuTrade


class StdScr:
    def __init__(self, stdscr):
        self.config = config
        self.code_list = self.config['Order.Stock'].get('CodeList').split(',')
        self.stdscr = stdscr
        self.config = config
        self.sub_type = [SubType.K_1M, SubType.K_5M, SubType.K_DAY]
        self.port = int(self.config['FutuOpenD.Config'].get('Port'))
        self.host = str(self.config['FutuOpenD.Config'].get('Host'))
        self.quote_ctx = OpenQuoteContext(host=self.host,
                                          port=self.port)
        self.trade_ctx = OpenSecTradeContext(filter_trdmarket=TrdMarket.HK,
                                             host=self.host,
                                             security_firm=SecurityFirm.FUTUSECURITIES)
        self.trading = FutuTrade(self.quote_ctx, self.trade_ctx)
        self.trading.kline_subscribe(self.code_list, self.sub_type)

    def get_stock(self, stock, yesterday):
        s = []
        i = 0
        for key, value in stock.items():
            data = self.trading.get_history_kline(key, KLType.K_DAY, start_date=yesterday,
                                                  end_date=yesterday)
            yesterday_close = data['close'][0]
            re, cur_data = self.trading.quote_ctx.get_cur_kline(key, 1, KLType.K_DAY, AuType.QFQ)
            today_close, today_high, today_low = cur_data['close'][0], cur_data['high'][0], cur_data['low'][0]
            amplitude = str(round((today_high - today_low) / today_low * 100, 2)) + '% '
            m = 'down ' + str(round((yesterday_close - today_close) / today_close * 100, 2)) + '%'
            if today_close >= yesterday_close:
                m = 'up ' + str(round((today_close - yesterday_close) / yesterday_close * 100, 2)) + '%'

            temp = [i, key, str(today_close), m, str(today_high), str(today_low), str(amplitude)]
            s.append(temp)
            i += 1
        return s

    def run(self):
        curses.curs_set(0)
        max_y, max_x = self.stdscr.getmaxyx()
        header = ["No", "stock", "close", "change_rate", "high", "low", "amplitude"]
        num_cols = len(header)
        col_width = max_x // num_cols

        # todo 从配置文件获取
        stock = {
            'HK.800000': '指数',
            'HK.00700': '腾讯',
            'HK.03690': '美团',
            'HK.09988': '阿里'
        }

        trade_res = self.trading.request_trading_days()
        yesterday = trade_res[-2]
        while True:
            time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            self.stdscr.clear()
            self.stdscr.addstr(0, 0, "Fixed text that will not change")
            data = self.get_stock(stock, yesterday)
            for i, col_name in enumerate(header):
                self.stdscr.addstr(2, i * col_width, col_name.center(col_width))

            for row_num, row_data in enumerate(data):
                for col_num, cell_data in enumerate(row_data):
                    self.stdscr.addstr(
                        row_num + 3,
                        col_num * col_width,
                        str(cell_data).center(col_width)
                    )
            self.stdscr.addstr(8, 0, "Current time is: {}".format(time_str))
            self.stdscr.refresh()
            time.sleep(2)
            key = self.stdscr.getch()
            if key == ord('q'):
                break
        curses.endwin()


def main(stdscr):
    my_app = StdScr(stdscr)
    my_app.run()


if __name__ == '__main__':
    curses.wrapper(main)
