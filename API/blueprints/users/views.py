from flask import Blueprint,request
from models.user import User
from flask.json import jsonify
from werkzeug.security import generate_password_hash , check_password_hash
from flask_jwt_extended import (create_access_token , create_refresh_token , jwt_refresh_token_required , get_jwt_identity , get_raw_jwt)
from flask_jwt_extended import jwt_required
import API.utils.jwt_helper

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['GET'])
def index():
    selected_users = User.select()
    result = jsonify({
        'data' : [u.as_dict() for u in selected_users]
    })
    return result

@users_api_blueprint.route('/new', methods=['POST'])
def create():
    data = request.form
    hashed_password = generate_password_hash(data['password'])

    new_user = User(
        email = data['email'],
        username = data['username'],
        password = hashed_password
    )

    new_user.save()

    successfully_created = (User.get_or_none( User.username ==  new_user.username ) != None)

    result = jsonify({
        'status' : successfully_created,
        'data': new_user.as_dict()
    })

    return result

@users_api_blueprint.route('/login',methods=['POST'])
def login():
    
    email = request.form['email']
    password = request.form['password']

    user_obj = User.get_or_none(User.email==email)
    user_found = (user_obj != None)

    access_token=None
    refresh_token=None
    login=False
    returned_data=None

    if user_found:
        if check_password_hash(user_obj.password,password):
            access_token = create_access_token(identity=user_obj.as_dict())
            refresh_token = create_refresh_token(identity=user_obj.as_dict())
            returned_data = user_obj.as_dict()
            login=True
        else:
            user_obj = None
    
    result = jsonify({
        'status':(user_found and login),
        'data':returned_data,
        'access_token':access_token,
        'refresh_token': refresh_token

    })

    return result