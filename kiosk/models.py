import json
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from kiosk import db
from kiosk import login

from kiosk.utils import log_func, entering, exiting

# flask-migrate alembic in use to manage db changes
# Use cmdline >flask db migrate -m "short message"
# to generate migration script. Inspect script if desired.
# Then cmdline >flask db upgrade
# to upgrade database from model changes in code.

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    orders = db.relationship('Orders', backref='customer', lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return f'<User {self.username}>'

    @log_func(entering, exiting)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    @log_func(entering, exiting)
    def check_password(self, password):
        # adding check for 0 length password hash in db
        try:
            return check_password_hash(self.password_hash, password)
        except AttributeError:
            return 0


class Session(db.Model):
    id = db.Column(db.String(256), primary_key=True)

    def __repr__(self):
        return f'{self.id}'


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orders = db.Column(db.String(1024), index=False, unique=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))

    def __repr__(self):
        orders = self.orders
        order_dict = {'Orders': orders}
        return json.dumps(order_dict)
    
    @log_func(entering, exiting)
    def save_order(items):
        """Saves the user's cart to the db"""
        pass


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(64), index=True, unique=True)
    price = db.Column(db.Float(10,2), index=False, unique=False)
    description = db.Column(db.Text, index=False, unique=False)
    img = db.Column(db.String(256), index=False, unique=False)
    options = db.Column(db.Text, index=False, unique=False)

    def __repr__(self):
        return f'<Item {self.item}>'