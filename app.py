import sys
from threading import Thread
from dataclasses import dataclass
from src import parse_api as api
from src import logger_config

@dataclass
class MainClass:
    log_main = logger_config.log_app('main')

    @classmethod
    def api_func(cls):
        api.dependencies()
        if api.api_check():
            try:
                Thread(target=api.proccessed_data_setup).start()
                Thread(target=api.rollover).start()
                Thread(target=api.auto_req).start()
                Thread(target=api.man_req).start()
                cls.log_main.info('All threads started, app running')
                while True:
                    user = input("Enter 'exit' to exit: ")
                    if user == 'exit':
                        return cls.api_func()
            except KeyError as error:
                cls.log_main.error(error)
                sys.exit()

if __name__ == '__main__':
    MainClass.api_func()