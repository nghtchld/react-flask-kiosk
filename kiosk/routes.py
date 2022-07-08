from kiosk import app
from kiosk import db

import os
import sys
from datetime import datetime
from collections import namedtuple
from flask import render_template, redirect, make_response, flash, url_for, session, send_from_directory, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from kiosk.forms import LoginForm, RegisterForm, EditProfileForm, MenuItemForm
from kiosk.models import User, Food
from kiosk.db_utils import init_food_table, register_user_in_db
from kiosk.config import Config

from kiosk.utils import log_func, entering, exiting
# from kiosk.utils import log_debug
# log_debug()

config = Config()

if config.SALT in (None, ""):
    app.logger.critical(".env does not contain critical 'SALT' value. Cannot continue.")
    sys.exit(1)
elif len(config.SALT) < 8:
    app.logger.critical(".env contains a 'SALT' value that is too short. Cannot continue.")
    sys.exit(1)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


#-# BEGIN ROUTE DECLARATIONS #-#
@app.route("/")
@app.route('/index')
def index():
    if current_user.is_authenticated:
        user = current_user
        username = user.username
    else:
        username = "Stranger"
    app.logger.debug(f"/index username is: {username}")
    flash('Test FLASH message!')
    return render_template("index.html.jinja", title="Home", username=username)


@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        register_user_in_db(form)
        username=form.username.data
        user = User.query.filter_by(username=username).first()
        app.logger.info(f"Logging in newly registered db user: {user}. With username {username}")
        login_user(user, remember=form.remember_me.data)
        app.logger.info(f"current_user is: {current_user}")
        flash(f'Congratulations {username}, you are now a registered Mex&Co Compradre!')
        return redirect(url_for('index'))
    return render_template('register.html.jinja', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        app.logger.debug(f"Checking username: '{username}'...")
        user = User.query.filter_by(username=username).first()
        if user is None:
            app.logger.info(f"Unknown user. Redirecting to 'register'.")
            return redirect(url_for('register'))
        elif user.password_hash is None or len(user.password_hash) == 0:
            db.session.delete(user)
            return redirect(url_for('register'))
        elif not user.check_password(password):
            flash('Invalid username or password')
            app.logger.info('Invalid password!')
            return redirect(url_for('login'))
        app.logger.info(f"Logging in db user: {user}. With username {username}")
        login_user(user, remember=form.remember_me.data)
        app.logger.info(f"User '{current_user.username}' has logged in.")
        # Check for a next (page) URL argument
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html.jinja', title='Sign In', form=form)


@app.route('/logout')
def logout():
    app.logger.info(f"User '{current_user.username}' has logged out.")
    logout_user()
    return redirect(url_for('index'))


# Solution from Flask Mega-Tutorial, also added <href...favicon.ico> in template.html.jinja
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'res'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/userpage/<username>')
@login_required
def userpage(username):
    app.logger.info("/userpage retrieving user.")
    user = User.query.filter_by(username=username).first_or_404()
    # TODO add list of user's orders, favorites etc using a _sub template
    # below are temp placeholder 'orders' by user 'user'
    orders = [
        {'customer': user, 'order': 'Test order #1'},
        {'customer': user, 'order': 'Test order #2'}
    ]
    # sample actual order code might be like:
    # orders = user.orders.all()
    return render_template('userpage.html.jinja', user=user, orders=orders)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    app.logger.info("/edit_profile creating form.")
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html.jinja', title='Edit Profile', form=form)


@app.route("/cart")
def cart():
    # app.logger.debug('CART TEST')
    # Temporary
    app.logger.info("/cart defining namedtuple.")
    Item = namedtuple('Item','foodID, name, price, description, image, options')
    cart = [
        Item("1", "Chicken", 10, "White meat", "/res/default.png", {}),
        Item("2", "Beef", 20, "Red meat", "/res/default.png", {}),
        Item("3", "Pork", 30, "Other white meat", "/res/default.png", {}),
        Item("4", "Fish", 40, "Sea meat", "/res/default.png", {})
    ]
    return render_template("cart.html.jinja", title="Cart", order=cart)


@app.route("/menu")
def menu():
    """
    Pulls menu items from Food model table and list them
    """
    # check Food table for contents
    init_food_table()
    menu_list = []
    menu = Food.query.all()
    for row in menu:
        menu_list.append([row.id, row.item, round(row.price,2), row.description, row.img])
    return render_template("menu.html.jinja", title="Menu", menu=menu_list)


@app.route("/menu/<itemname>", methods=["GET", "POST"])
def menu_item(itemname):
    """
    Details of the menu item with number to order selection form.
    """
    app.logger.info(f"Selecting item from db: '{itemname}'...")
    food = Food.query.filter_by(item=itemname).first_or_404()
    if not food:
        app.logger.debug(f"Sorry! Sold out of '{itemname}. Please select a different item.")
    app.logger.info(f"Retrieved item from db")#: '{food}', name: {food.item}.")
    #title = ' '.join('Order your', food.item)

    form = MenuItemForm(default=itemname)
    if form.validate_on_submit():
        name = food.item
        number = form.number.data
        price = round(food.price, 2)
        app.logger.debug(f"name: {name}, number: {number}, price: {price}")
        cost = number * price
        flash(f"{number} {name}s added to your cart. That will cost ${cost}.")
    return render_template("menu_item.html.jinja", title="Order Menu Item", form=form, food=food)
    pass

@app.route("/cart/<int:id>")
def cartItem(id):
    return make_response(render_template("403.html.jinja"), 403)


@app.route("/403")
def forboden():
    return make_response(render_template("403.html.jinja"), 403)

#-# SPECIAL ROUTES #-#

@app.errorhandler(404)
def not_found(e):
    return make_response(render_template("404.html.jinja"), 404)

@app.errorhandler(403)
def forbidden(e):
    return make_response(render_template("403.html.jinja"), 403)

@app.after_request
def after_request(r):
    # Set headers to prevent caching
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r