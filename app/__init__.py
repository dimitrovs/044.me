from app.api import api
from bson import ObjectId
from flask.json import JSONEncoder
from flask import Flask, send_from_directory
import sys
sys.path.append("../web/static")

STATIC_FOLDER = "../web/static"


class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return JSONEncoder.default(self, o)


app = Flask(__name__,
            static_url_path='',
            static_folder=STATIC_FOLDER)

app.json_encoder = CustomJSONEncoder
app.register_blueprint(api, url_prefix="/api")


@app.route('/')
def _home():
    return send_from_directory(STATIC_FOLDER, 'index.html')
