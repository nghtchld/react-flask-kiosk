import os
import csv
import logging as log
from kiosk import app, db
from kiosk.models import Food, User
from kiosk.utils import log_func, entering, exiting
# from kiosk.utils import log_debug
# log_debug()

@log_func(entering, exiting)
def init_food_table():
    # Make sure there is data in the main.foods TABLE
    app.logger.debug(f"Checking Food model table for contents:")
    menu = Food.query.all()
    app.logger.debug(f"Got: {menu}")
    if len(menu) < 2:
        app.logger.info('Reading menu file...')
        filePath = os.path.join(app.root_path, 'res','menu.csv')
        app.logger.debug(f"filepath is: {filePath}")
        reader = csv.DictReader(open(filePath))
        app.logger.info('Inserting menu items from menu.csv to Food model table...')
        for row in reader:
            app.logger.debug(f"Menu row: {row}")#['item']}, {row['price']}, {row['description']}")
            food = Food(item=row['item'],
                        price=row['price'],
                        description=row['description'],
                        img=row['img'],
                        options=row['options'])
            db.session.add(food)
            db.session.commit()
    else:
        app.logger.debug(f"Food model table contains: {len(menu)} items.")


@log_func(entering, exiting)
def register_user_in_db(form):
    username = form.username.data
    email = form.email.data
    password = form.password.data
    u = User(username=username, email=email, password=password)
    db.session.add(u)
    db.session.commit()
    #return render_template('register.html.jinja', form = form)