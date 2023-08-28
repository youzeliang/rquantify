import json, requests, time

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

    def __init__(self):
        pass

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
