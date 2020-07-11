from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
import requests
import os
import taglib


app = Flask(__name__)
app.config.from_object(Config)

bootstrap=Bootstrap(app)

try:
    os.mkdir("app/static/encodedsamples")
except FileExistsError:
    pass

file=requests.get("https://i.ibb.co/jfPhg0Y/sample-ORIG.png")
with open("app/static/sample.png", "wb+") as op:
    op.write(file.content)

file=requests.get("https://i.ibb.co/DMTg9LX/pcb-3374102-1280.png")
with open("app/static/sample2.png", "wb+") as op:
    op.write(file.content)

from app import routes


