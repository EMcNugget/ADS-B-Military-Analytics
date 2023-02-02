import logging
import logging.handlers
import os

class Logger:
    def __init__(self, app_name):
        if not os.path.exists(os.path.join(os.getcwd(), "logs")):
            os.makedirs(os.path.join(os.getcwd(), "logs"))
        self.logger = logging.getLogger(f'{app_name}')
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.file_handler = logging.handlers.RotatingFileHandler(
            f'{os.path.join(os.getcwd(), "logs/adsb_main.log")}',
            maxBytes=1000000, mode='w', backupCount=5)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

def log_app(app_name):
    logger = Logger(app_name)
    return logger.logger
