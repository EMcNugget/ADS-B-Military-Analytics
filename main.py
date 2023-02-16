"""Main app file for the project."""
from threading import Thread
from dataclasses import dataclass
from server import parse_api as api
from server import logger_config
from server import analytics as an

@dataclass
class MainClass:
    """Main class for the project."""
    log_main = logger_config.log_app('main')

    @classmethod
    def api_func(cls):
        """Main function for the project."""
        api.dependencies()
        if api.api_check():
            Thread(target=api.proccessed_data_setup).start()
            Thread(target=api.rollover).start()
            Thread(target=api.auto_req).start()
            cls.log_main.info('All threads started, app running')


if __name__ == '__main__':
    Thread(target=MainClass.api_func()).start()
    an.app.run(debug=False, host='0.0.0.0', port=5000)
