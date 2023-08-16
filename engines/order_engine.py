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
