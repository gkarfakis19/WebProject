import os


class Config(object):
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'supersikrit123'
    UPLOAD_FOLDER=os.environ.get("UPLOAD_FOLDER") or "/app/upload"
