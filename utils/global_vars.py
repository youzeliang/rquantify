import configparser

from pathlib import Path

PATH = Path.cwd()

PATH_CONFIG = PATH.parent / 'config'

print(PATH_CONFIG)
config = configparser.ConfigParser()
config.read(
    PATH_CONFIG / 'config.ini' if (PATH_CONFIG / 'config.ini').is_file() else PATH_CONFIG / 'config_template.ini')
