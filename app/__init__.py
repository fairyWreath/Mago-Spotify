from flask import Flask, session
from config import Config
from flask_session import Session
from flask_bootstrap import Bootstrap

import os

app = Flask(__name__)
app.config.from_object(Config)

caches_folder = './.spotify_caches/'
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)

Session(app)
bootstrap = Bootstrap(app)

from app import routes