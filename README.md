# Restaurant Kiosk: a React front-end Flask back-end (api) Web App
This repo contains a [Flask](https://palletsprojects.com/p/flask/) web application with an [sqlite](https://sqlite.org/) dev database using flask-sqlalchemy Classes. It broadly follows the [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).
This fork adds React.js for the front end development and uses more resources from [Miguel Grinberg](https://blog.miguelgrinberg.com/) as well as other React.js tutorials;

# Features
- Working flask/jinja website with templates (HTML, JS, CSS)
- Working flask-sqlalchemy defined sqlite (dev) database setup with initial data insertion
- Working Flask-WTF forms
- Working clean up testform.py, main.py
- Working session username usage (only for index atm)
- Working menu read from db to menu page
- Working logging uses wrappers and decorators for functions
    see https://towardsdatascience.com/using-wrappers-to-log-in-python
- Working Flash messages on all templates
- Working Demo React.js front end using demo (docker) Microblog app
Up to here - see current work plan section, below:
- TODO Replace Microblog demo app with Kiosk app
- TODO Ordering system using flask-sqlalchemy Classes
- TODO Menu item customisation on orders
- TODO Receipt prodcution with Tax and Tip
- TODO Admin Panel (Ability to create discounts, Foods and customisations )
- TODO Add SMTP server for sending emails (see below link for needed .env vars)
    https://blog.miguelgrinberg.com/post/the-react-mega-tutorial-chapter-5-connecting-to-a-back-end
- TODO add Unit testing: https://realpython.com/python-testing/
    https://code.visualstudio.com/docs/python/testing
- TODO Containerise (Docker): https://code.visualstudio.com/docs/containers/quickstart-python
- TODO Deploy to cloud (AWS, Azure): https://code.visualstudio.com/docs/python/python-on-azure
https://docs.microsoft.com/en-us/azure/app-service/quickstart-python?tabs=flask%2Cwindows%2Cazure-cli%2Cvscode-deploy%2Cdeploy-instructions-azportal%2Cterminal-bash%2Cdeploy-instructions-zip-azcli&pivots=python-framework-flask

# Installation
## Install npm and create a project template
`npx create-react-app react-flask-app`
`cd react-flask-app`

## Git clone this repo into subfolder `kiosk-app`

## Use venv for virtual environment setup
`cd into\the\kiosk-app\folder`
`py -m venv venv --upgrade-deps`

## Activate virtual env and generate a better requirements.txt with pip-tools
`.\kiosk-app\venv\Scripts\activate.bat`

`pip install -r requirements.txt`

`pip freeze > requirements.in`

Edit the `requirements.in` file above to only list the packages from the original requirements.txt

`py -m piptools compile --output-file=requirements.txt requirements.in`

## Create a .env file in root folder (or use ENV variables)
a root `.env` file is needed by `/kiosk/config.py` for at least a SALT (> 8 characters long) and a DATABASE name defined. Its template is:
    DATABASE=app.db
    DATABASE_URL=
    SALT=must_have_a_salt_more_than_8_chrs_long
    SECRET_KEY=
    PORT=
for email functions using a free SendGrid account. https://app.sendgrid.com/guide/integrate/langs/python 
- add Auth later, false for now
    DISABLE_AUTH=true
    MAIL_SERVER=smtp.sendgrid.net
    MAIL_PORT=587
    MAIL_USE_TLS=true
    MAIL_USERNAME=apikey    # <-- this is the literal word "apikey"
    MAIL_PASSWORD=          # <-- your SendGrid API key here
    MAIL_DEFAULT_SENDER=reactjs@nghtchld.com    # <-- the sender email address you'd like to use

## Initialise the database
The app uses the flask-migrate package and so the database schema is under Alembic control. The Alembic migration scripts are in the `/migrations` folder.

Before running the flask app you need to create and initialise the database.
1. run flask db init (creates a database and sets up migrations)
2. run flask db migrate (creates the upgrade script)
3. run flask db upgrade (upgrades the database to the latest version)

# TEMP TODO install demo Microblog app in a Docker for dev of React
https://blog.miguelgrinberg.com/post/the-react-mega-tutorial-chapter-5-connecting-to-a-back-end
`docker-compose up -d`
`docker-compose run --rm microblog-api bash -c "flask fake users 10"`
`docker-compose run --rm microblog-api bash -c "flask fake posts 100"`

# Running the front and back end apps
from `.\kiosk-app\`
`yarn start` Starts React.js front end. Confirm it is running at: http://localhost:3000
`yarn start-kiosk` Starts Flask back end.

# Licence
This project is licenced under the BSD 3-Clause licence. A full copy of this licene is in the `LICENCE` file.

# Current work plan
TODO Ordering system using flask-sqlalchemy Classes
## Needed
* Food details page of form 'menu\<item>'
* Dropdown number to orders selection form -> displayed on food details page
* Do we then have to write the item selection immediately to the db?
** or can we store in 'session' and if so how?
** and then when do we write to the db?

## Fixes needed
* change menu_list in route /menu to namedtuple
* change menu.html for item loop to use namedtuple names in place of list [ints]
