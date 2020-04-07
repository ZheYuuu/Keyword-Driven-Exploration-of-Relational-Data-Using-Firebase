import os
from dotenv import load_dotenv
import pyrebase

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    pass

FirebaseConfig = dict(
    apiKey = os.environ.get("apiKey"),
    authDomain = os.environ.get("authDomain"),
    databaseURL = os.environ.get("databaseURL"),
    storageBucket = os.environ.get("storageBucket"),
)

