import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin
from flask_wtf import CSRFProtect
from pymessenger.bot import Bot
from store.config import Config
from ipinfo import getHandler


ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')
IP_TOKEN = os.environ.get('IP_TOKEN')

bot_handler = Bot(ACCESS_TOKEN)
handler = getHandler(IP_TOKEN)

db = SQLAlchemy()
bcrypt= Bcrypt()
login_manager= LoginManager()
admin= Admin()
csrf= CSRFProtect()

def create_App(config=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.app_context().push()

    db.init_app(app)
    bcrypt.init_app(app)
    admin.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view= 'users.login'
    login_manager.login_message_category= 'info'

    from store.users.routes import users
    from store.bot.routes import bot
    from store.main.routes import main
    from store.errors.handlers import errors
    from store.logic.routes import logic

    #app.register_blueprint(users)
    app.register_blueprint(bot)
    app.register_blueprint(main)
    #app.register_blueprint(errors)
    #app.register_blueprint(logic)

    return app