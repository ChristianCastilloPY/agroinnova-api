import bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
import urllib.request
import json

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(120), nullable=False)
    l_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hashed_password = db.Column(db.String(480), nullable=False)
    salt= db.Column(db.String(250), nullable=False)
    rol = db.Column(db.String(20), nullable=False)
    url_image = db.Column(db.String(250))
    created_at = db.Column(db.DateTime(timezone=True),  default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),  onupdate=func.now())
    is_active = db.Column(db.Boolean(), nullable=False)


    def __repr__(self):
        return f'<User {self.email}>'
    
    @classmethod
    def create(cls, body):
        try:
            user_is_valid = cls.user_exist(email=body.get("email"))
            if isinstance(user_is_valid, cls):
                raise Exception({
                    "message": "Invalid user",
                    "status": 400
                })
            if(user_is_valid) != False:
                raise Exception({
                    "message": "Internal application error",
                    "status": 500
                })
            
            salt_bytes = bcrypt.gensalt()
            salt = salt_bytes.decode()
            hashed_password = generate_password_hash(f'{body["password"]}{salt}')
            new_user = cls(f_name=body["f_name"], l_name=body["l_name"], rol="admin", email=body["email"], hashed_password=hashed_password, salt=salt, is_active=True, url_image=body["url_image"])
            if not isinstance(new_user, cls):
                raise Exception({
                    "message": "Internal application error",
                    "status": 500
                })
            saved = new_user.save_and_commit()
            if not saved:
                raise Exception({
                    "message": "Database error",
                    "status": 500
                })
            return new_user
        except Exception as error:
            return error.args[0]

    @classmethod
    def user_exist(cls, **kwargs):
        try:
            user_exist = cls.query.filter_by(email=kwargs["email"]).one_or_none()
            if user_exist:
                user = cls(id=user_exist.id ,email=user_exist.email, hashed_password=user_exist.hashed_password, salt=user_exist.salt, created_at=user_exist.created_at, updated_at=user_exist.updated_at)
                return user
            return False
        except Exception as error:
            return error.args[0]
            
    @classmethod
    def verify_credentials(cls, **kwargs):
        try:
            user = cls.user_exist(email=kwargs["email"])
            if not isinstance(user, cls):
                raise Exception({
                    "message": "Invalid user or password",
                    "status": 400
                })
            password_is_valid = check_password_hash(user.hashed_password, f'{kwargs["password"]}{user.salt}')
            if not password_is_valid:
                raise Exception({
                    "message": "Invalid user or password",
                    "status": 400
                })
            return user
        except Exception as error:
            return error.args[0]
    
    @classmethod
    def update_user(cls, body, user_id):
        try:
            user = cls.query.get(user_id)
            if body.get("f_name"):
                user.f_name = body["f_name"]
            if body.get("l_name"):
                user.l_name = body["l_name"]
            if body.get("l_name"):
                user.l_name = body["l_name"]
            if body.get("password"):
                hashed_password = generate_password_hash(f'{body["password"]}{user.salt}')
                user.hashed_password = hashed_password
            if body.get("url_image"):
                user.url_image = body["url_image"]
            db.session.commit()
            return user
        except Exception as error:
            return error.args[0]

    def save_and_commit(self):
        """
            Salva la instancia creada, en la base de datos. Si sucede algún error, 
            se retorna False y se revierten los cambios de la sesión
        """
        try:
            db.session.add(self)  #Guardamos la instancia en la sessión
            db.session.commit() #Creamos el registro en la db 
            return True
        except Exception as error:
            db.session.rollback() #Retornamos a la session mas reciente
            return False

    def serialize(self):
        return {
            "id": self.id,
            "f_name": self.f_name,
            "l_name": self.l_name,
            "email": self.email,
            "rol": self.rol,
            "url_image": self.url_image,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_active": self.is_active,
        }