"""Main app file for the project."""
from threading import Thread
from server import app

def api_func():
    """Main function for the project."""
    if app.api_check():
        Thread(target=app.Main.auto_req).start()
        Thread(target=app.rollover).start()

if __name__ == '__main__':
    Thread(target=api_func()).start()
    app.app.run(host='0.0.0.0', port=8080, debug=True)
