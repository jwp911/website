from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

#__init__.py makes the website folder a package and defines/configures
    #the app and connections to MySQL, BCrypt, and LoginManager.
app = Flask(__name__)
app.config['SECRET_KEY'] = '65468A4D1H654FDSG64SFD65'
uri_string = 'mysql+mysqlconnector://mysqladmin:GreenEnergy2024!@192.168.0.4:3306/db'
app.config['SQLALCHEMY_DATABASE_URI'] = uri_string
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

#Tutorial said to import this, not sure if it is required
from website import routes

