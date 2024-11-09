import json, requests, time
import json
import requests

from utils import logger
from utils.global_vars import *

order_url = 'http://127.0.0.1:12344/order/insert'
position_url = 'http://127.0.0.1:12344/query/position'
account_url = 'http://127.0.0.1:12344/query/account'
queue_order_url = 'http://127.0.0.1:12344/query/order'
trade_url = 'http://127.0.0.1:12344/query/trade'
cancel_url = 'http://127.0.0.1:12344/order/cancel'
modify_url = 'http://127.0.0.1:12344/order/modify'

header = {
    "Content-Type": "application/json",
    "Charset": "UTF-8"
}


class OrderEngine:

    def __init__(self, quote_ctx: OpenQuoteContext, trade_ctx: OpenSecTradeContext):
        self.default_logger = logger.Logger().logger
        self.quote_ctx = quote_ctx
        self.trade_ctx = trade_ctx
        self.trd_env = TrdEnv.REAL

    def get_order_list(self):
        """
        查询多日订单,默认当日
        :return:
        """
        # https://openapi.futunn.com/futu-api-doc/trade/get-order-list.html，每3s 才能请求一次
        ret_code, order_list_data = self.trade_ctx.order_list_query(order_id="", trd_env=self.trd_env,
                                                                    start=time.strftime("%Y-%m-%d", time.localtime()),
                                                                    refresh_cache=False)

        if ret_code != RET_OK:
            self.default_logger.error(f"Cannot acquire order list {order_list_data}")
            return None
        return order_list_data

    def place_order(self, code: str, side: str, exchange: str, type: str, price: str, qty: int):
        """
        :param code:
        :param qty:
        """
        data = {
            "clord_id": 'api_' + str(int(time.time())),
            "exchange": exchange,
            "symbol": code,
            "side": side,
            "open_close": "",
            "qty": qty,
            "type": type,
            "price": price,
            "tif": "DAY",
            "allow_eth": "YES"
        }

        res = json.loads(requests.post(order_url, headers=header, json=data).text)
        error_id = res['error_id']
        error_msg = res['error_msg']
        if error_id != '0' or error_msg != '':
            return

        order_id = res['order_id']

        return order_id

    def z_cancel(self, order_id: str):
        """
        取消订单
        :param order_id:
        :return:
        """
        data = {
            "order_id": order_id
        }

        try:
            res = json.loads(requests.post(cancel_url, headers=header, json=data).text)
            error_id = res['error_id']
            error_msg = res['error_msg']
            if error_id != '0' or error_msg != '':
                self.logger.error(error_msg)
        except Exception as e:
            self.logger.error(e)
