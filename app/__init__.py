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

if app.config['LOG_TO_STDOUT']:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)
else:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/mago.log',
                                        maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

app.logger.setLevel(logging.INFO)
app.logger.info('Mago startup')


from app import routes