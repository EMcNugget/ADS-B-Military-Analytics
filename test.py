import api_processor as ap
import data_processor as dp
from threading import Thread
import loggerConfig


LG_MAIN = loggerConfig.log_app('test')


def main():
    user = input("Enter 'ap' to start api_processor.py or 'dp' to start data_processor.py: ")
    if user == "ap":
        if ap.api_check():
            try:
                ap.dependencies()
                Thread(target=ap.proccessed_data_setup).start() # removes API logging and renames dict
                Thread(target=ap.rollover).start() # starts a new proccessed data file every day
                Thread(target=ap.auto_req).start() # automatically fetches data from API
                Thread(target=ap.man_req).start() # manual option to fetch data from API
                LG_MAIN.info('All threads started, app running')
            except Exception as e:
                LG_MAIN.error(e)
        else:
            exit()


    elif user == "dp":
        dpUser = input("Enter df to start data_format() or 't1' to start remove_test1234(): ")
        if dpUser == "df":
            dp.data_format()
        elif dpUser == "t1":
            dp.remove_test1234()
    else:
        print("Invalid input")
