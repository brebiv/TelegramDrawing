from flask import Flask, render_template, request
from queue import Queue
import base64
from PIL import Image
from io import BytesIO

# Disable console messages
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


"""
app.add_url_rule: https://flask.palletsprojects.com/en/1.1.x/api/?highlight=add#flask.Flask.add_url_rule
"""


class ServerWrapper:

    def __init__(self, queue: Queue):
        self.app = Flask(__name__)
        self.app.add_url_rule("/<string:hash>", 'index', self.index)
        self.app.add_url_rule("/getImage/<string:hash>", 'getImage', self.getImage, methods=["POST"])
        self.q = queue

    def index(self, hash: str):
        return render_template('index.html')

    def getImage(self, hash: str):
        print(hash)
        img_data = request.get_data()
        raw_data = img_data.decode("UTF-8").split(",")[1].encode()
        image = Image.open(BytesIO(base64.b64decode(raw_data)))
        self.q.put(image)
        return "Ok"

    def run(self):
        self.app.run("0.0.0.0")
