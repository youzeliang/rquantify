import configparser
from futu import *
from pathlib import Path

PATH = Path.cwd()

PATH_CONFIG = PATH.parent / 'config'

print(PATH_CONFIG)
config = configparser.ConfigParser()
config.read(
    PATH_CONFIG / 'config.ini' if (PATH_CONFIG / 'config.ini').is_file() else PATH_CONFIG / 'config_template.ini')

index_k = {0: 'K_1M', 1: 'K_3M', 2: 'K_5M', 3: 'K_15M', 4: 'K_30M', 5: 'K_60M', 6: 'K_DAY', 7: 'K_WEEK', 8: 'K_MON',
           9: 'K_YEAR'}

index_type = {0: KLType.K_1M, 1: KLType.K_3M, 2: KLType.K_5M, 3: KLType.K_15M, 4: KLType.K_30M, 5: KLType.K_60M,
              6: KLType.K_DAY, 7: KLType.K_WEEK,
              8: KLType.K_MON,
              9: KLType.K_YEAR}

futu_api = {
    '1': {
        'cookie': 'xxxxxxx',
        'quote-token': 'xxxxxxx'},
    '0': {
        'cookie': 'xxxx',
        'quote-token': 'xxx'},

}

ignore = [
    '天然气', '芝加哥', '营建', 'ISM', '进口物价', '工业产出', '房产市场数据', '原油库存', '战略石油', '成品油',
    '经济状况褐皮书', '丽莎', '鲍曼', '经常帐', '费城', '商业', '房价指数', '里奇', '新屋', '谘商', '成屋', '贸易帐',
    '石油钻井', '社会用电量', '短期能源', '全球支付', '房产市场指数', '个人支出月率', '耐用品', '职位空缺', '批发销售',
    '威廉姆斯', '电量数据', '戴利', '博斯蒂克', '阿波利斯', '达拉斯联储', '明尼阿波利', '沃勒', '哈玛克', '库格勒',
    '穆萨莱姆', '国债竞拍', '杰斐逊', '零售销售', '巴尔']
