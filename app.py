import sys
from threading import Thread
from src import api_processor as ap
from src import data_processor as dp
from src import logger_config

def main():
    log_main = logger_config.log_app('main_app')
    user = input("Enter 'api' to start the API proccessor, 'data' to start the data processor, or 'exit' to exit: ")
    if user == 'api':
        if ap.api_check():
            try:
                ap.dependencies()
                Thread(target=ap.proccessed_data_setup).start()
                Thread(target=dp.rollover).start()
                Thread(target=ap.auto_req).start()
                Thread(target=ap.man_req).start()
                log_main.info('All threads started, app running')
            except KeyError as error:
                log_main.error(error)
                sys.exit()
    elif user == 'data':
        try:
            # WIP
            log_main.info('Data processor threads started')
        except KeyError as error:
            log_main.error(error)
            sys.exit()
    elif user == 'exit':
        sys.exit()

    else:
        print("Invalid input")
        log_main.warning("Invalid input")
        return main()

if __name__ == "__main__":
    main()


# --todo--

# Intergrate timing logic to utilize data_processor.py

# -Intergrate data analytics with Pandas UPDATE 2/3/2023: Halfway done

# --Future--

# -Create front end with PyPQt6

# -Web version? Probably Django or Flask for the backend,
# I'm out of the loop when it comes to web development so I'm not sure what would be best for the front end
