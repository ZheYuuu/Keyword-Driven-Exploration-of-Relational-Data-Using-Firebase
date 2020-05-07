from flask import Flask 
from config import Config, FirebaseConfig
from flask_cors import CORS
import pyrebase
import logging

# Fix pyrebase bug: double encoding url rejection
# https://github.com/thisbejim/Pyrebase/issues/294
def noquote(s):
    return s
pyrebase.pyrebase.quote = noquote

def create_app(config_class=Config):
    app = Flask(__name__)
    # app.debug=True
    
    app.config.from_object(config_class)

    # Enable CORS
    CORS(app)
    # Register blueprint
    from app.api import bp
    app.register_blueprint(bp, url_prefix='/api')

    return app

def connect_firebase(config_dict=FirebaseConfig):
    firebase = pyrebase.initialize_app(FirebaseConfig)
    db = firebase.database()
    return db 

db = connect_firebase()
