import unittest
from app import create_app, db
from tests import TestConfig, TestMixin
import json
from const import train, prov, station

class TrainTestCase(TestMixin):
    def setUp(self):
        super().setUp()
        self.client = self.app.test_client()
        self.base_url = '/api/china_train/'

    def test_train_list(self):
        endpoint = train 
        url = f"{self.base_url}{endpoint}/"
        headers = {'page':0, 'page_size':10}
        response = self.client.get(url, headers=headers)
        data = json.loads(response.data)
        self.assertIn('_meta',data)
        
    def test_prov_list(self):
        endpoint = prov 
        url = f"{self.base_url}{endpoint}/"
        headers = {'page':0, 'page_size':10}
        response = self.client.get(url, headers=headers)
        data = json.loads(response.data)
        self.assertIn('_meta',data)

    def test_station_list(self):
        endpoint = station 
        url = f"{self.base_url}{endpoint}/"
        headers = {'page':0, 'page_size':10}
        response = self.client.get(url, headers=headers)
        data = json.loads(response.data)
        self.assertIn('_meta',data)