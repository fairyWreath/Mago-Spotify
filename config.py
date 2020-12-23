import os

class Config:
    SECRET_KEY = os.urandom(64)
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = './.flask_session/'

    # for heroku logs
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

    