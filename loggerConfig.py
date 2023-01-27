import logging
import logging.handlers
import os
import time 


class Logger:
    def __init__(self, app_name):
        self.logger = logging.getLogger(f'{app_name}')
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.file_handler = logging.handlers.RotatingFileHandler(
            'adsb_main.log', maxBytes=1000000, mode='w', backupCount=5)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)


def log_app(app_name):
    logger = Logger(app_name)
    return logger.logger


def rotator():
    try:
        if os.path.exists('adsb_main.log'):
            os.rename(f'adsb_main_{int(time.time())}.log')
        else:
            pass
    except OSError as e:
        Logger('logging').logger.error(e)
