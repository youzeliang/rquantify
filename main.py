import hmac
import base64
import os
import sys
from flask import Flask, request

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from utils import global_vars

from futu import *

from strategies.response import OResponse

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def get_data():
    if request.method == "POST":
        timestamp = request.headers.get('Timestamp')
        sign = request.headers.get('Sign')
        if check_sig(timestamp) == sign:
            req_data = json.loads(str(request.data, 'utf-8'))
            logger.get_logger(log_dir=logger.LOG_FILE).info(req_data)
            r = OResponse(req_data['text']['content'].strip(), req_data['sessionWebhook'], req_data['senderStaffId'],
                          logger.get_logger(log_dir=logger.LOG_FILE)
                          )
            r.handle_text_info()
    return 's'


def check_sig(timestamp):
    app_secret = str(global_vars.config['DingTalk'].get('AppSecret'))
    string_to_sign = '{}\n{}'.format(timestamp, app_secret)
    hmac_code = hmac.new(app_secret.encode('utf-8'), string_to_sign.encode('utf-8'), digestmod=hashlib.sha256).digest()
    sign = base64.b64encode(hmac_code).decode('utf-8')
    return sign


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088)
