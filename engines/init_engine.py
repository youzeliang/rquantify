import os, sys

from utils.global_vars import *

from futu import *

from trading_engine import FutuTrade


class Init:
    def __init__(self):
        """
        init some config and others
        """
        self.config = config
        self.port = int(self.config['FutuOpenD.Config'].get('Port'))
        self.host = str(self.config['FutuOpenD.Config'].get('Host'))
        self.code_list = self.config['Order.Stock'].get('CodeList').split(',')

        # self.ignore_code = self.config['Order.Stock'].get('IgnoreCodeList').split(',')

        self.sub_type = [SubType.K_1M, SubType.K_5M, SubType.K_DAY]

        self.quote_ctx = OpenQuoteContext(host=self.host,
                                          port=self.port)
        self.trade_ctx = OpenSecTradeContext(filter_trdmarket=TrdMarket.HK,
                                             host=self.host,
                                             security_firm=SecurityFirm.FUTUSECURITIES)
        self.monitor = FutuTrade(self.quote_ctx, self.trade_ctx)

        self.monitor.kline_subscribe(self.code_list, self.sub_type)


if __name__ == '__main__':
    pass
