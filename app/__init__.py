from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS



# Create an instance of Flask class
app = Flask(__name__)
# Configuring our app with Attributes and Values from the Config class --> CREATED AFTER CREATION OF FORMS!!!! <-- app.config['SECRET_KEY'] = 'you-will-never-guess > moved to config.py folder!
app.config.from_object(Config)

# Add CORS to our app
CORS(app)

# Create an instance of SQLAlchemy to represent our database
db = SQLAlchemy(app) # the app as instance of Flask
# Create an instance of migrate to track our database migrations
migrate = Migrate(app, db)
# Create an instance of LoginManager to handle authentication
login = LoginManager(app)
# login.login_view = 'login'
login.login_view = 'login'

# register the api blueprint with our app
from .blueprints.api import api
app.register_blueprint(api)

# import routes
from . import routes, models