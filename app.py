from flask import Flask, send_from_directory

# app libraries
from api import api

STATIC_FOLDER = "web/static"

app = Flask(__name__,
            static_url_path='',
            static_folder=STATIC_FOLDER)

app.register_blueprint(api, url_prefix="/api")


@app.route('/')
def _home():
    return send_from_directory(STATIC_FOLDER, 'index.html')
