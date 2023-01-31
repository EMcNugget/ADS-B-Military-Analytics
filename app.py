import src.api_processor as ap
import src.data_processor as dp
import src.logger_config as logger_config
from threading import Thread

def main():
    LG_MAIN = logger_config.log_app('main_app')
    user = input("Enter 'api' to start the API proccessor, 'data' to start the data processor, or 'exit' to exit: ")
    if user == 'api':
        if ap.api_check():
            try:
                ap.dependencies()
                Thread(target=ap.proccessed_data_setup).start() # removes API logging and renames dict
                Thread(target=dp.rollover).start() # starts a new proccessed data file every day
                Thread(target=ap.auto_req).start() # automatically fetches data from API
                Thread(target=ap.man_req).start() # manual option to fetch data from API
                LG_MAIN.info('All threads started, app running')
            except Exception as e:
                LG_MAIN.error(e)
                exit()
    elif user == 'data':
        try:
            dp.remove_dup()
            dp.remove_test1234()
            LG_MAIN.info('Data processor threads started')
        except Exception as e:
            LG_MAIN.error(e)
            exit()
    elif user == 'exit':
        exit()

    else:
        print("Invalid input")
        LG_MAIN.warning("Invalid input")
        return main()

if __name__ == "__main__":
    main()


# --todo--

# Intergrate data_proccessor.py logic into app.py

# -Intergrate data analytics with Pandas

# -Refactor data processing with Pandas, still exploring the possibilities of this

# --Future--

# -Create front end with PyPQt6

# -Web version? Probably Django or Flask for the backend, I'm out of the loop when it comes to web development so I'm not sure what would be best for the front end