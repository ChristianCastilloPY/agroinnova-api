import os
from flask_admin import Admin
from models import db, User
from flask_admin.contrib.sqla import ModelView
from flask_jwt_extended import JWTManager

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
    admin = Admin(app, name='SISPYCOM', template_mode='bootstrap3')
    jwt = JWTManager(app)
    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))