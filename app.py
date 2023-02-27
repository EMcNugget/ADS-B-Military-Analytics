import os
import datetime
from flask import Flask, Response, jsonify
from flask_cors import CORS
from markupsafe import escape
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

MDB_URL = os.environ["MDB_URL"]
cluster = MongoClient(MDB_URL)
db = cluster["milData"]
collection = db["historicalData"]


@app.route('/<date>/<specified_file>', methods=['GET'])
def get_mdb_data(date: str, specified_file: str):
    """Date will be in YYYY-MM-DD format, provided by the UI, then
    the file will be pulled from the database or cache, and returned to the UI"""

    results = collection.find_one({"_id": date})
    try:
        if results is None:
            try:
                datetime.date.fromisoformat(date)
                return Response(status=400, response=f'Data for {escape(date)} not found in database')
            except ValueError:
                return Response(status=500, response='Invalid date format. Please use YYYY-MM-DD format.')
        else:
            try:
                response_data = results[specified_file]
            except KeyError:
                return Response(status=400, response=f'File {escape(specified_file)} not found for {escape(date)}')
            return jsonify(response_data)
    except TypeError:
        return Response(status=500, response='Invalid date format. Please use YYYY-MM-DD format.')

@app.route('/')
def default():
    """Default route"""
    return Response(status=400, response='Please specify a date and file')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
