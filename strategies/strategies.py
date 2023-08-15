from datetime import date
import time


def valid_time():
    """
    判断当前时间是否在交易时间内 todo 剔除掉节假日
    :return:
    """
    str_today = str(date.today())
    stamp = int(time.mktime(time.strptime(str_today + ' 09:30:00', '%Y-%m-%d %H:%M:%S')))
    stamp_twelve = int(time.mktime(time.strptime(str_today + ' 11:59:00', '%Y-%m-%d %H:%M:%S')))
    stamp_thirteen = int(time.mktime(time.strptime(str_today + ' 12:59:00', '%Y-%m-%d %H:%M:%S')))
    stamp_fourteen = int(time.mktime(time.strptime(str_today + ' 16:00:00', '%Y-%m-%d %H:%M:%S')))
    exit_flag = False
    now = int(time.time())
    if stamp_fourteen <= now:
        exit_flag = True

    if now < stamp or (stamp_twelve <= now <= stamp_thirteen):
        return True, exit_flag
    return False, exit_flag


class QuoteChange:

    def __init__(self):
        pass
