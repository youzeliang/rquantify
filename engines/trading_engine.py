from futu import *
from datetime import date
from utils import logger

from typing import List, Any, Dict


class FutuTrade:

    def __init__(self, quote_ctx: OpenQuoteContext, trade_ctx: OpenSecTradeContext):
        self.quote_ctx = quote_ctx
        self.trade_ctx = trade_ctx
        self.logger = logger.get_logger(log_dir=logger.LOG_FILE)

    def get_hk_stocks(self) -> dict:
        output_dict = {}

        simple_filter = SimpleFilter()
        simple_filter.stock_field = StockField.CUR_PRICE
        simple_filter.filter_min = 2
        simple_filter.is_no_filter = False

        market_val = SimpleFilter()
        market_val.stock_field = StockField.MARKET_VAL
        market_val.filter_min = 100000000000  # one billion
        market_val.is_no_filter = False

        turnover = AccumulateFilter()
        turnover.stock_field = StockField.TURNOVER
        turnover.filter_min = 10000000  # one ten million
        turnover.is_no_filter = False

        sum_of_business = FinancialFilter()
        sum_of_business.stock_field = StockField.SUM_OF_BUSINESS
        sum_of_business.filter_min = 10000000
        sum_of_business.is_no_filter = False
        sum_of_business.quarter = FinancialQuarter.ANNUAL  # year

        financial_filter = AccumulateFilter()
        financial_filter.stock_field = StockField.VOLUME
        financial_filter.filter_min = 200000  # daily volume
        financial_filter.is_no_filter = False

        lot_price = SimpleFilter()
        lot_price.stock_field = StockField.LOT_PRICE
        lot_price.filter_min = 2000
        lot_price.is_no_filter = False

        begin_index = 0

        ignore_stock = {}
        for i in range(0, len(self.init.ignore_code)):
            ignore_stock[self.init.ignore_code[i]] = self.init.ignore_code[i]

        while True:
            ret, ls = self.init.quote_ctx.get_stock_filter(market=Market.HK,
                                                           filter_list=[simple_filter, market_val, turnover,
                                                                        sum_of_business,
                                                                        lot_price, financial_filter],
                                                           begin=begin_index)
            if ret == RET_OK:
                last_page, all_count, ret_list = ls
                for item in ret_list:
                    if item.stock_code in ignore_stock.keys():
                        continue
                    output_dict[item.stock_code] = item.stock_name
                begin_index += 200
                if begin_index >= all_count:
                    break
            elif ret == RET_ERROR:
                self.logger.error(f'get_stock_filter err: \n{output_dict}')
                return output_dict
        self.logger.info(f'get_stock_filter: \n{output_dict}')
        output_dict['HK.HSImain'] = "恒指主连"
        output_dict['HK.800000'] = "恒生指数"
        output_dict['HK.07226'] = "南方两倍做多恒生科技"
        output_dict['HK.07552'] = "南方两倍做空恒生科技"
        return output_dict

    def get_history_kline(self, stock_code, ktype,
                          start_date=str(date.today().year - 2) + '-' + str(date.today().month) + '-' + str(
                              date.today().day), end_date=str(date.today())):
        column_names = ['open', 'close', 'high', 'low', 'volume', 'turnover', 'change_rate', 'last_close', 'time_key']
        history_df = pd.DataFrame(columns=column_names)
        ret, data, page_req_key = self.quote_ctx.request_history_kline(stock_code,
                                                                       start=start_date,
                                                                       end=end_date,
                                                                       ktype=ktype, autype=AuType.QFQ,
                                                                       fields=[KL_FIELD.ALL],
                                                                       max_count=1000, page_req_key=None,
                                                                       extended_time=True)
        if ret == RET_OK:
            history_df = pd.concat([history_df, data], ignore_index=True)
            time.sleep(0.6)
        else:
            self.logger.error('request_history_kline.%s', data)
        while page_req_key is not None:
            ret, data, page_req_key = self.quote_ctx.request_history_kline(stock_code,
                                                                           start=start_date,
                                                                           end=end_date,
                                                                           ktype=ktype, autype=AuType.QFQ,
                                                                           fields=[KL_FIELD.ALL],
                                                                           max_count=1000,
                                                                           page_req_key=page_req_key,
                                                                           extended_time=True)
            if ret == RET_OK:
                history_df = pd.concat([history_df, data], ignore_index=True)
            else:
                self.logger.error(f'page data, Cannot request_history_kline: {history_df}')
                return

        return history_df

    def request_trading_days(self, start_date=str(date.today().year - 2) + '-' + str(date.today().month) + '-' + str(
        date.today().day), end_date=str(date.today())) -> List[Any]:
        """
        请求交易日，该交易日是通过自然日剔除周末和节假日得到，未剔除临时休市数据。
        :param start_date: 默认从今天往过去2年取交易日
        :param end_date:
        :return: [{'time': '2020-04-01', 'trade_date_type': 'WHOLE'}, ...]
        """

        ret, data = self.quote_ctx.request_trading_days(market=TradeDateMarket.HK, start=start_date,
                                                        end=end_date)
        if ret == RET_OK:
            l = list()
            for i in range(0, len(data)):
                l.append(data[i]['time'])
            return l
        else:
            print('error:', data)

    def kline_subscribe(self, stock_list: list, sub_type: list) -> bool:
        self.logger.info(f'Subscribing to {len(stock_list)} kline...')
        ret_sub, err_message = self.quote_ctx.subscribe(stock_list, sub_type)
        if ret_sub != RET_OK:
            self.logger.error(f'Cannot subscribe to K-Line: {err_message}')
            return False
        return ret_sub == RET_OK
