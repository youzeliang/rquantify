import json
import requests


# def convertible_bonds(self):
#     """
#     可转债
#     :return:
#     """
#     if h == 9 and 30 <= m <= 40:
#         if self.init.redis.get("convertible") is not None:
#             return
#         url = 'https://api.mrxiao.net/kzz'
#         try:
#             s = ''
#             today_list = json.loads(requests.get(url).text)['today_start_kzz']
#             if len(today_list) > 0:
#                 for i in range(0, len(today_list)):
#                     s += '  ' + today_list[i]['SECURITY_NAME_ABBR']
#                 s_loggers.Logger(filename=s_loggers.LOG_FILE_CONVER).logger.info(s)
#                 self.init.cov.send_ding_message(s, True)
#                 self.init.redis.set("convertible", s, ex=60 * 60 * 8)
#         except Exception as e:
#             self.default_logger.error('convertible_bonds-err', e)
#             self.init.own_dingtalk.send_ding_message('可转债接口异常', True)
