import unittest
from app import create_app, db
from tests import TestConfig, TestMixin
import json
import urllib

class WorldTestCase(TestMixin):
    def setUp(self):
        super().setUp()
        self.client = self.app.test_client()
        self.base_url = '/api/world'

    def test_city_list(self):
        endpoint = 'city'
        url = f"{self.base_url}/{endpoint}/"
        headers = {'page':0, 'page_size':10}
        response = self.client.get(url, headers=headers)
        data = json.loads(response.data)
        self.assertIn('_meta',data)
        
    def test_country_list(self):
        endpoint = 'country'
        url = f"{self.base_url}/{endpoint}/"
        headers = {'page':0, 'page_size':10}
        response = self.client.get(url, headers=headers)
        data = json.loads(response.data)
        self.assertIn('_meta',data)

    def test_countrylanguage_list(self):
        endpoint = 'countrylanguage'
        url = f"{self.base_url}/{endpoint}/"
        headers = {'page':0, 'page_size':10}
        response = self.client.get(url, headers=headers)
        data = json.loads(response.data)
        self.assertIn('_meta',data)
    
    def test_keywordsearch(self):
        endpoint = 'index'
        url = f"{self.base_url}/{endpoint}?"
        headers = {'page':0, 'page_size':10}
        payload = {'keyword':'English'}
        params = urllib.parse.urlencode(payload)
        response = self.client.get(url+params, headers=headers)
        data = json.loads(response.data)



    