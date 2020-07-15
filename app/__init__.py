from flask import Flask, flash, request, redirect, url_for
import flask_uploads
from config import Config
from flask_bootstrap import Bootstrap
import requests
import os

UPLOADED_PHOTOS_ALLOW={'png'}
UPLOADED_PHOTOS_DEST='app/static/Uploads'
UPLOADS_DEFAULT_DEST= "app/static/Uploads"

UPLOAD_FOLDER = 'app/static/Uploads'
ALLOWED_EXTENSIONS = {'png'}

app = Flask(__name__)
app.config.from_object(Config)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["UPLOADED_PHOTOS_DEST"]=UPLOADED_PHOTOS_DEST
app.config["UPLOADED_PHOTOS_ALLOW"]=UPLOADED_PHOTOS_ALLOW
app.config["UPLOADS_DEFAULT_DEST"]=UPLOADS_DEFAULT_DEST
app.config["ALLOWED_EXTENSIONS"]=ALLOWED_EXTENSIONS

photos = flask_uploads.UploadSet('photos', flask_uploads.IMAGES)
flask_uploads.configure_uploads(app,photos)

bootstrap=Bootstrap(app)

try:
    os.mkdir("app/static/encodedsamples")
    os.mkdir("app/static/Uploads")
except FileExistsError:
    pass

file=requests.get("https://i.ibb.co/jfPhg0Y/sample-ORIG.png")
with open("app/static/sample2.png", "wb+") as op:
    op.write(file.content)

file=requests.get("https://i.ibb.co/DMTg9LX/pcb-3374102-1280.png")
with open("app/static/sample.png", "wb+") as op:
    op.write(file.content)

from app import routes


