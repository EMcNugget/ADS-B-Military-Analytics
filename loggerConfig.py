import logging
import logging.handlers
import os 
import datetime
    
class Logger:
    def __init__(self, app_name):
        self.logger = logging.getLogger(f'{app_name}')
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.file_handler = logging.handlers.RotatingFileHandler(
            f'{os.path.join(os.path.dirname(__file__), "Logs/adsb_main.log")}', maxBytes=1000000, mode='w', backupCount=5)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

def log_file_system():
    loggingPath = os.path.join(os.path.dirname(__file__), 'Logs\\')
    if not os.path.exists(loggingPath):
        os.makedirs(loggingPath)
    with open(loggingPath + 'adsb_main.log', 'w') as log_file:
        Logger('adsb_main').logger.info(f'Application started at {datetime.datetime.now()}')

def log_app(app_name):
    logger = Logger(app_name)
    return logger.logger