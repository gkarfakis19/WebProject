from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
import requests
import os
app = Flask(__name__)
app.config.from_object(Config)

bootstrap=Bootstrap(app)

os.mkdir("app/static/encodedsamples")

# if os.path.exists("app/static/encodedsamples"): #this doesnt
#     print("app/static")
#
# if os.path.exists("app/static/sample.png"): #this exists
#     print("img found too")

file=requests.get("http://res.cloudinary.com/gkwebsite/image/upload/sample_rtt6io.png")
with open("app/static/sample.png", "wb+") as op:
    op.write(file.content)

file=requests.get("http://res.cloudinary.com/gkwebsite/image/upload/sample.png")
with open("app/static/sample2.png", "wb+") as op:
    op.write(file.content)

from app import routes


