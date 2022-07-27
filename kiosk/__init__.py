# @name Restaurant Kiosk
# @author: Ash Skabo
# @author: Stuart Skabo
# @year: 2022
# @copyright: BSD 3-Clause licence
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Config

# Define the flask app
app = Flask(__name__, static_folder="res")
# setup flask-login module
login = LoginManager(app)
login.login_view = 'login'

# setup flask config
app.config.from_object(Config)

# import logging
from kiosk.utils import log_debug
log_debug()

# setting up sqlalchemy and alembic
app.logger.info("Setting up SQLAlchemy...")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.logger.info("SQLAlchemy initialised")

# check default data is in database
from kiosk.db_utils import init_food_table, init_user_table
init_food_table()
init_user_table()

# setup flask routes
app.logger.info("Importing routes...")
from kiosk import routes, models, errors
app.logger.info("Finished importing routes, models, errors")
