"""Flask API that returns data from MongoDB"""

import os
import datetime
from flask import Flask, Response, jsonify
from flask_cors import CORS
from flask_caching import Cache
from markupsafe import escape
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})


MDB_URL = os.environ['MDB_URL']
cluster = MongoClient(MDB_URL)
db = cluster["milData"]
collection = db["historicalData"]


@app.route('/<date>/<specified_file>', methods=['GET'])
def get_mdb_data(date: str, specified_file: str):
    """Date will be in YYYY-MM-DD format, provided by the UI, then
    the file will be pulled from the database or cache, and returned to the UI"""

    try:
        date_val = escape(datetime.date.fromisoformat(date))
    except ValueError:
        return Response(status=400, response='Invalid date format. Please use YYYY-MM-DD format.')

    cached_data = cache.get(f"{date_val}{specified_file}")
    if cached_data is not None:
        return jsonify(cached_data)
    results = collection.find_one({"_id": date_val})

    if date_val > datetime.date.today().isoformat():
        return Response(status=400, response='There is no data from the future.', mimetype='text/plain')
    if date_val < '2023-03-09':
        return Response(status=400, response='There is no data from before 2023-02-27', mimetype='text/plain')
    if results is None:
        return Response(status=404, response=f'Data for {date_val} not found in database')
    try:
        final_results = results[specified_file]
        cache.set(f"{date_val}{specified_file}", final_results, timeout=120)
        return jsonify(final_results)
    except KeyError:
        return Response(status=406, response=f'File {escape(specified_file)} not found for {date_val}')


@app.route('/')
def default():
    """Default route"""
    return Response(status=400, response='Please specify a date and file')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
