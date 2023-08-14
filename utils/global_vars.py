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
