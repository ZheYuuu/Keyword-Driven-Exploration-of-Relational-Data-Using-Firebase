import unittest
from app import create_app, db
from tests import TestConfig, TestMixin
from const import daily, area, date
import json
import urllib


class CoronavirusTestCase(TestMixin):
    def setUp(self):
        super().setUp()
        self.client = self.app.test_client()
        self.base_url = "/api/coronavirus"

    def test_daily_situation_list(self):
        endpoint = daily
        url = f"{self.base_url}/{endpoint}/"
        headers = {"page": 0, "page_size": 10}
        response = self.client.get(url, headers=headers)
        data = json.loads(response.data)
        self.assertIn("_meta", data)

    def test_area_list(self):
        endpoint = area
        url = f"{self.base_url}/{endpoint}/"
        headers = {"page": 0, "page_size": 10}
        response = self.client.get(url, headers=headers)
        data = json.loads(response.data)
        self.assertIn("_meta", data)

    def test_statisic_list(self):
        endpoint = date
        url = f"{self.base_url}/{endpoint}/"
        headers = {"page": 0, "page_size": 10}
        response = self.client.get(url, headers=headers)
        data = json.loads(response.data)
        self.assertIn("_meta", data)


    def test_keywordsearch(self):
        endpoint = 'index'
        url = f"{self.base_url}/{endpoint}?"
        headers = {'page':0, 'page_size':10}
        payload = {'keyword':'Tennessee'}
        params = urllib.parse.urlencode(payload)
        response = self.client.get(url+params, headers=headers)
        data = json.loads(response.data)
        self.assertGreater(len(data), 0)