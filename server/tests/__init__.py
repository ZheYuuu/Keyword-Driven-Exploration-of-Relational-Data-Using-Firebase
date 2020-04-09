from config import Config, FirebaseConfig
import unittest
from app import create_app, db

class TestConfig(Config):
    TESTING =True 

class TestMixin(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        self.app_context.pop()
