from src.server import analytics as an

an.app.run(host='127.0.0.1', port=5000, threaded=True, debug=True)

# production WSGI server will reside here