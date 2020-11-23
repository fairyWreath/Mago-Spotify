import os

class Config:
    SECRET_KEY = os.urandom(64)
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = './.flask_session/'
    