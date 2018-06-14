from flask import Flask
from flask_cors import CORS
from base import RedisConfig

app = Flask(__name__, static_folder='../static')

from app import views, string, prompt

CORS(app, supports_credentials=True)


