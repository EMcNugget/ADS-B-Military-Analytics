import bin.api_processor as ap
import bin.data_processor as dp
import bin.loggerConfig as loggerConfig
from threading import Thread


LG_MAIN = loggerConfig.log_app('main_app')

def main():
    user = input("Enter 'api' to start the API proccessor, 'data' to start the data processor, or 'exit' to exit: ")
    loggerConfig.log_file_system()
    if user == 'api':
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

# Work on Docker, Still learning how to use it

# Update naming conventions

# Fix loggerConfig.py log rollover funtion

# Update file system to be more organized

# Intergrate data_proccessor.py logic into app.py

# -Intergrate data analytics with NumPy and Matplotlib (Perhaps Pandas, still working on which one would be better for this project) 

# --Future--

# -Create front end with PyPQt6

# -Web version? Probably Django or Flask for the backend, I'm out of the loop when it comes to web development so I'm not sure what would be best for the front end