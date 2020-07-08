from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
import cloudinary

app = Flask(__name__)
app.config.from_object(Config)

bootstrap=Bootstrap(app)

im=cloudinary.CloudinaryImage("sample_rtt6io.jpg").image(quality=100)
f=open("app/static/sample2.png","w+")
f.write(im)
f.close()

from app import routes


