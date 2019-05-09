from flask import Blueprint,request
from models.user import User
from flask.json import jsonify
from models.blog import Blog
from flask_jwt_extended import jwt_required

blogs_api_blueprint = Blueprint('blogs_api',
                             __name__,
                             template_folder='templates')


@blogs_api_blueprint.route("/",methods=['GET']) # all blogs
def index():
    b_query = Blog.select()
    b_list = []

    for i in b_query:
        b_list.append(i.as_dict())

    result = jsonify({
        'data':b_list
    })

    return result

@blogs_api_blueprint.route('/new',methods=['POST']) #create
@jwt_required
def create():
    data = request.form

    new_b = Blog.create(
        parent_user = data['user_id'],
        title = data['title'],
        d = data['d'],
    )

    new_b.save()

    result = jsonify({
        'status':True,
        'data' : new_b.as_dict()
    })

    return result
@blogs_api_blueprint.route("/edit",methods=["POST"]) #edit
@jwt_required
def edit():
    data = request.form
    target_b = Blog.get_or_none(Blog.id==data['blog_id'])

    target_b.title = data['blog_title']
    target_b.desc = data['blog_d']

    if target_b.save():
        success = True
    
    result = jsonify({
        'status' : success,
        'data' : target_b.as_dict()
    })

    return result

@blogs_api_blueprint.route('/delete',methods=["POST"]) #delete
@jwt_required
def delete():
    deletion_id = int(request.form['blog_id'])
    Blog.delete().where(
        Blog.id==deletion_id
    ).execute()

    successfully_deleted = Blog.get_or_none(Blog.id == deletion_id)

    result = jsonify({
        'status': successfully_deleted
    })

    return result

@blogs_api_blueprint.route('/<id>',methods=["GET"])
def show(id):

    blog = Blog.get_or_none(Blog.title==id)
    b_found = blog!=None
    result = jsonify({
        'status':b_found,
        'data':blog.as_dict()
    })

    return result