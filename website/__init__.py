from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
import os

db = SQLAlchemy()
mail = Mail()
DB_NAME = 'database.db'
ALLOWED_EXTENSIONS = {'image/png', 'image/jpeg'}
picFolder = os.path.join('static', 'images')

def createApp():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'stefannemanja'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['UPLOAD_FOLDER'] = picFolder
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_USERNAME'] = 'throwaway82678@gmail.com'
    app.config['MAIL_PASSWORD'] = 'H3m1jsk!D8'
    app.config['MAIL_POST'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    mail.init_app(app)
    
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    createDatabase(app)

    loginManager = LoginManager()
    loginManager.login_view = 'auth.login'
    loginManager.init_app(app)

    @loginManager.user_loader
    def loadUser(id):
        return User.query.get(int(id))

    return app

def createDatabase(app):
    if not os.path.exists('website/' + DB_NAME):
        db.create_all(app=app)
