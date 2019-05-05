from app import app 
from flask_jwt_extended import JWTManager
from models.user import User
import os

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['JWT_TOKEN_LOCATION'] = ['headers']
jwt = JWTManager(app)