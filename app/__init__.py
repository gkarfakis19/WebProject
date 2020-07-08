from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from PIL import Image
import requests

app = Flask(__name__)
app.config.from_object(Config)

bootstrap=Bootstrap(app)

file=requests.get("http://res.cloudinary.com/gkwebsite/image/upload/sample_rtt6io.png")
with open("app/static/sample.png", "wb+") as op:
    op.write(file.content)

file=requests.get("http://res.cloudinary.com/gkwebsite/image/upload/sample.png")
with open("app/static/sample2.png", "wb+") as op:
    op.write(file.content)

from app import routes


