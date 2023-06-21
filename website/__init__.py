from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from website.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'user_bp.login'
login_manager.login_message_category = 'info'

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    from website.users.routes import users
    from website.posts.routes import posts
    from website.main.routes import main
    from website.errors.handlers import errors
    app.register_blueprint(users, name = 'user_bp')
    app.register_blueprint(posts, name = 'post_bp')
    app.register_blueprint(main, name = 'main_bp')
    app.register_blueprint(errors, name = 'err_bp')

    return app

