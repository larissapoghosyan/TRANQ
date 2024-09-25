import os


class Config(object):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Directory of the config.py file
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    # SECRET_KEY = "2afefd91ed46b4083975f5e6f468f9f37ed19124b8c034aceb7dc0f780672695"
    DATABASE = os.path.join(BASE_DIR, 'trip.db')
    DEBUG = True
