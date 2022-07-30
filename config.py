import os
from dotenv import load_dotenv

load_dotenv("./.env")

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY') or 'you-will-never-guess-bijillity-bloo'
    PORT = os.getenv('PORT', '5000')
    SALT = os.getenv('SALT')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, os.environ.get('DATABASE'))
    print( 'sqlite:///' + os.path.join(basedir, os.environ.get('DATABASE')))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['reactjs@nghtchld.com']