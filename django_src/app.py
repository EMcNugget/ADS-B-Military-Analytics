import sys
from threading import Thread
from dataclasses import dataclass
from .custom_src import parse_api as api
from .custom_src import logger_config
from .custom_src import analytics as an

@dataclass
class MainClass:
    user: str = input("Enter 'api' to run the API, 'data' to run the data processor, or 'exit' to exit: ")
    log_main = logger_config.log_app('main')

    @classmethod
    def api_func(cls):
        if cls.user == 'api':
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
    @classmethod
    def type_func(cls):
        data, data2 = input("Enter date in YYYY-MM-DD format, and the requested type: ").split()
        return an.Analytics.for_data(date=data, info_req=data2)

    @classmethod
    def int_func(cls):
        data2 = input("Enter date in YYYY-MM-DD format: ")
        return an.Analytics.inter_ac(date=data2)

def main():
    api.dependencies()
    if MainClass.user == 'api':
        MainClass.api_func()
    elif MainClass.user == 'antype':
        MainClass.type_func()
    elif MainClass.user == 'anint':
        MainClass.int_func()
    elif MainClass.user == 'exit':
        sys.exit()

if __name__ == "__main__":
    main()
