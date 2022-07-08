# Don't know if anything in this file is used apart from: 
# SQLALCHEMY_DATABASE_URI
# SQLALCHEMY_TRACK_MODIFICATIONS
# These (all?) can go in the .flaskenv file

import os
from dotenv import load_dotenv


load_dotenv("./.env")

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY') or 'you-will-never-guess'
    PORT = os.getenv('PORT', '5000')
    SALT = os.getenv('SALT')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, os.environ.get('DATABASE'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False