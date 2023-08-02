from utils.global_vars import *

from futu import *


class FutuTrade:

    def __init__(self):
        self.config = config

        self.host = str(self.config['FutuOpenD.Config'].get('Host'))
        self.port = int(self.config['FutuOpenD.Config'].get('Port'))

        self.quote_ctx = OpenQuoteContext(host=self.config['FutuOpenD.Config'].get('Host'),
                                          port=self.config['FutuOpenD.Config'].getint('Port'))
        self.trade_ctx = OpenHKTradeContext(host=self.config['FutuOpenD.Config'].get('Host'),
                                            port=self.config['FutuOpenD.Config'].getint('Port'))
