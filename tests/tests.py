"""Tests for both GAE and GCE backends"""

import os
from unittest import TestCase, main
import requests
from dotenv import load_dotenv
from pymongo import MongoClient, errors

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_HOST = os.getenv("API_HOST")
MDB_URL = os.getenv("MDB_URL")


class TestGCEBackendComponents(TestCase):
    """Tests various backend functions that run on Google Compute Engine"""

    def test_api_connection(self):
        """Tests the connection to the ADS-B Exchange API"""

        url = "https://adsbexchange-com1.p.rapidapi.com/v2/mil/"
        headers = {
            "X-RapidAPI-Key": API_KEY,
            "X-RapidAPI-Host": API_HOST
        }
        response = requests.request(
            "GET", url, headers=headers, timeout=5)  # type: ignore
        self.assertEqual(response.status_code, 200)

    def test_mongodb_connection(self):
        """Tests the connection to MongoDB"""

        client = MongoClient(MDB_URL)
        try:
            client.server_info()
        except errors.ServerSelectionTimeoutError as err:
            print(err)
            self.fail("MongoDB connection failed")
        finally:
            client.close()


if __name__ == '__main__':
    main()
