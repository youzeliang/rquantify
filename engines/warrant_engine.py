from futu import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from utils.global_vars import *
import utils.util


class Warrant:

    def __init__(self, quote_ctx: OpenQuoteContext):
        """
        Futu Warrant Engine Constructor
        :param quote_ctx:
        """
        self.config = config
        self.quote_ctx = quote_ctx
        self.logger = logger.get_logger(log_dir=logger.LOG_FILE)

    def get_warrant(self, stock_code, code_type, vol_min=utils.util.warrant_vol(), conversion_max=10000,
                    conversion_min=10000, num=50,
                    cur_price_min=0.07,
                    cur_price_max=0.2):
        req = WarrantRequest()
        req.status = WarrantStatus.NORMAL
        req.sort_field = SortField.VOLUME
        req.issuer_list = ["SG", "BP", "CS", "JP", "UB"]
        req.ascend = False
        req.street_max = 35
        req.conversion_max = conversion_max
        req.conversion_min = conversion_min
        req.leverage_ratio_min = 10
        req.vol_min = vol_min
        req.num = num
        req.cur_price_min = cur_price_min
        req.cur_price_max = cur_price_max

        if code_type == 'bear':
            req.type_list = WrtType.BEAR
        elif code_type == 'all':
            req.type_list = [WrtType.BEAR, WrtType.BULL]
        else:
            req.type_list = WrtType.BULL

        ret, ls = self.quote_ctx.get_warrant(stock_code, req)
        if ret == RET_OK:
            warrant_data_list, last_page, all_count = ls
            if len(warrant_data_list) == 0:
                self.logger.error('富途暂未返回数据')
                return
            return warrant_data_list
        self.logger.error(ret)
        return []
