import os, sys

from utils.global_vars import *

from futu import *


class Init:
    def __init__(self):
        """
        init some config and others
        """
        self.config = config
        self.port = int(self.config['FutuOpenD.Config'].get('Port'))
        self.host = str(self.config['FutuOpenD.Config'].get('Host'))
        # self.ignore_code = self.config['Order.Stock'].get('IgnoreCodeList').split(',')

        self.sub_type = [SubType.K_1M, SubType.K_5M, SubType.K_DAY]

        self.quote_ctx = OpenQuoteContext(host=self.host,
                                          port=self.port)
        self.trade_ctx = OpenSecTradeContext(filter_trdmarket=TrdMarket.HK,
                                             host=self.host,
                                             security_firm=SecurityFirm.FUTUSECURITIES)


if __name__ == '__main__':
    pass
