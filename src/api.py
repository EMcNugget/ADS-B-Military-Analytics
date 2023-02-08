import os
from flask import Flask, jsonify
from flask_restful import Api, Resource
from .analytics import get_mdb_data, day

app = Flask(__name__)
api = Api(app)
DEP_DEPENDENCY = os.getcwd() + '\\data\\'

# Error handling is taken care of in the file that the function resides in.
# So we don't need to worry about it here.

class Data(Resource):
    @app.route(f'/{day}', methods=['GET'])
    def query_data(self, info):
        return jsonify(get_mdb_data(day, info))

if __name__ == '__main__':
    app.run(debug = True)
