

##-# IMPORTS #-##
import os
import logging as log

from kiosk.config import Config

##-# DECLARATIONS & SET UP #-##

config = Config()

# Change path to own directory
# os.chdir(os.path.dirname(os.path.realpath(__file__)))

# If salt is not set or too short, exit.


## Connect to database
# now using SQLAlchemy in __init__.py

# # Make sure there is data in the main.foods TABLE
# menu = Food.query.all()
# app.logger.debug(f"Checking Food model table for contents:")
# app.logger.debug(f"{menu}")
# if len(menu) < 2:
#     filePath = os.path.join('res','menu.csv')
#     app.logger.info('Reading menu file...')
#     reader = csv.DictReader(open(filePath))
#     app.logger.info('Inserting menu items from menu.csv to Food model table...')
#     for row in reader:
#         app.logger.debug(f"Menu row: {row}")#['item']}, {row['price']}, {row['description']}")
#         food = Food(item=row['item'],
#                     price=row['price'],
#                     description=row['description'],
#                     img=row['img'],
#                     options=row['options'])
#         db.session.add(food)
#         db.session.commit()

# con.execute("SELECT name FROM main.foods")
# food_count = con.fetchall()
# app.logger.info(f'Menu length is: {str(len(food_count))}')
# if len(food_count) < 2:
#     app.logger.info('Inserting menu items from menu.csv to main.foods table...')
#     try:
#         # Fill main.foods table from menu.csv
#         con.execute("""COPY main.foods FROM 'menu.csv' (QUOTE '"', HEADER);
#                 """)
#     except NameError:
#         exc_type, exc_value, exc_traceback = sys.exc_info()
#         lines = log.traceback.format_exception(exc_type, exc_value, exc_traceback)
#         log.critical("Error loading data from menu.txt to TABLE main.foods:")
#         log.critical( ''.join('!! ' + line for line in lines))

# con.close()