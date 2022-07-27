from kiosk import app
from kiosk import db

import os
import time
import json
from datetime import datetime
from flask import render_template, redirect, make_response, flash, url_for, session, send_from_directory, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from kiosk.forms import CheckoutSubmitForm, LoginForm, RegisterForm, EditProfileForm, MenuItemForm
from kiosk.models import User, Food, Orders
from kiosk.db_utils import register_user_in_db, save_order_in_db

from kiosk.utils import order_totals

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

#-# BEGIN ROUTE DECLARATIONS #-#
# default routes
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

# React.js front end test route
@app.route('/time')
def get_current_time():
    return {'time': time.time()}


# Solution from Flask Mega-Tutorial, also added <href...favicon.ico> in template.html.jinja
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'res'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


# User route functions
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


@app.route('/userpage/<username>')
@login_required
def userpage(username):
    app.logger.info("/userpage retrieving user...")
    user = User.query.filter_by(username=username).first_or_404()
    app.logger.debug(f"user: {user}")
    # TODO add list of user's orders, favorites etc using a _sub template
    # below are temp placeholder 'orders' by user 'user'
    # orders_all = user.orders.all()
    orders_all = Orders.query.filter_by(user_id=user.id).all()
    app.logger.debug(f"users orders: {orders_all}")
    
    orders = []
    for order in orders_all:
        lines = []
        odq = order.orders.replace('\'', '"')
        order_line_list = json.loads(odq)
        for line in order_line_list:
            lines.append(line)
        orders.append({'when':order.timestamp, 'lines':lines})
    app.logger.debug(f"{orders}")
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


# Menu and ordering route functions
@app.route("/menu")
def menu():
    """
    Pulls menu items from Food model table and list them
    """
    # TODO remove after testing, Now done in __init__ 
    # init_food_table() # to check Food table for contents
    menu_list = []
    menu = Food.query.all()
    for row in menu:
        menu_list.append([row.id, row.item, round(row.price,2), row.description, row.img])
    return render_template("menu.html.jinja", title="Menu", menu=menu_list)


@app.route("/menu/<itemname>", methods=["GET", "POST"])
def menu_item(itemname):
    """
    Details of the menu item with number to orders selection form.
    """
    if 'orders' in session:
        app.logger.debug(f"initial orders is:{session['orders']}")
        pass
    else:
        session['orders'] = []
        app.logger.debug(f"initial orders is: empty list ({session['orders']})")        
    
    app.logger.info(f"Selecting item from db: '{itemname}'...")
    food = Food.query.filter_by(item=itemname).first_or_404()
    if not food:
        app.logger.debug(f"Sorry! Sold out of '{itemname}. Please select a different item.")
        flash(f"Sorry! Sold out of '{itemname}. Please select a different item.")
        return redirect(url_for('menu'))
    app.logger.info(f"Retrieved item '{itemname}' from db")#: '{food}', name: {food.item}.")

    form = MenuItemForm(default=itemname)
    if form.validate_on_submit():
        name = food.item
        number = form.number.data
        price = food.price
        app.logger.debug(f"name: {name}, number: {number}, price: {price}")
        cost = round(number * price, 2)
        flash(f"{number} {name}s added to your cart. That will cost ${cost}.")
        
        session['orders'].append({'item': food.item, 'number': form.number.data, 'cost': float(cost)})
        _, total = order_totals()
        flash(f"Your Order Total is: ${total.price}. To finish ordering, click on Cart")
        app.logger.debug(f"final orders is: {session['orders']}")
        return redirect(url_for('menu'))
    return render_template("menu_item.html.jinja", title="Orders Menu Item", form=form, food=food)


@app.route('/cart' , methods=['GET', 'POST'])
def cart():
    if 'orders' in session:
        cart, total = order_totals()
    else:
        flash('There is nothing in your cart! Order something yummy!')
        return redirect(url_for('menu'))

    app.logger.info("/cart submitting cart to checkout page.")
    form = CheckoutSubmitForm()
    if form.validate_on_submit():
        return redirect(url_for('checkout', cart=cart, total=total))
    
    return render_template("cart.html.jinja", title="Cart", cart=cart, total=total, form=form)


@app.route("/checkout")
def checkout():
    if 'orders' in session:
        order_id = save_order_in_db()
        cart, total = order_totals()
        session.pop('orders', None)
        session['order_id'] = order_id
    else:
        flash('There is nothing in your cart! Order something yummy!')
        return redirect(url_for('menu'))
    return render_template("checkout.html.jinja", cart=cart, total=total)


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