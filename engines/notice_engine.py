import os, sys
import socket

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from utils import logger

from engines.init_engine import Init


class Notice:

    def __init__(self):
        self.init = Init()
        self.logger = logger.get_logger(log_dir=logger.LOG_FILE)

    def check_port(self):
        """
        Check if the Futu port is started up correctly.

        :return:
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.init.host, self.init.port))
            s.shutdown(2)
            self.logger.info("port is open")
            return True
        except Exception as e:
            logger.get_logger(log_dir=logger.ERROR_LOG_FILE).error(e)
            return False


if __name__ == '__main__':
    s = Notice()
    s.check_port()
