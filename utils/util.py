import time
import datetime


def str_of_num(num):
    """
    成交量转化
    :param num:
    :return:
    """

    def strofsize(num, level):
        if level >= 2:
            return num, level
        elif num >= 10000:
            num /= 10000
            level += 1
            return strofsize(num, level)
        else:
            return num, level

    units = ['', '万', '亿']
    num, level = strofsize(num, 0)
    if level > len(units):
        level -= 1
    return '{}{}'.format(round(num, 2), units[level])


def trade_hk_time(l):
    """
    回撤时判断是否在港股交易时间
    :param l:
    :return:
    """
    today = l[:10]
    nine_stamp = int(time.mktime(time.strptime(today + ' 09:30:00', '%Y-%m-%d %H:%M:%S')))
    sixteen_stamp = int(time.mktime(time.strptime(today + ' 16:00:00', '%Y-%m-%d %H:%M:%S')))
    now_stamp = int(time.mktime(time.strptime(l, '%Y-%m-%d %H:%M:%S')))
    if now_stamp < nine_stamp or now_stamp > sixteen_stamp:
        return False
    return True


def day_time():
    t = time.localtime()
    n = t.tm_hour

    if 8 <= n <= 22:
        return True
    return False


def working_day():
    t = time.localtime()

    n = t.tm_wday
    if 0 <= n <= 4:
        return True
    return False