from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__)
app.config.from_object(Config)

bootstrap=Bootstrap(app)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

from app import routes


