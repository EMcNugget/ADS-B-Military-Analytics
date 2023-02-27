"""Main app file for the project."""
from threading import Thread
from .app import vm

def api_func():
    """Main function for the project."""
    Thread(target=vm.Main.auto_req).start()
    Thread(target=vm.rollover).start()

if __name__ == '__main__':
    api_func()