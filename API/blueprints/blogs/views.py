from flask import Blueprint,request
from models.user import User
from flask.json import jsonify
from models.blog import Blog
from flask_jwt_extended import jwt_required

blogs_api_blueprint = Blueprint('blogs_api',
                             __name__,
                             template_folder='templates')


@blogs_api_blueprint.route("/",methods=['GET'])
def index():
    blog_query = Blog.select()
    blog_list = []

    for b in blog_query:
        blog_list.append(b.as_dict())

    result = jsonify({
        'data':blog_list
    })

    return result


@blogs_api_blueprint.route('/new',methods=['POST'])
@jwt_required
def create():
    data = request.form

    new_blog = Blog.create(
        parent_user = data['user_id'],
        desc = data['desc'],
        title = data['title']
    )

    new_blog.save()

    result = jsonify({
        'status':True,
        'data' : new_blog.as_dict()
    })

    return result


@blogs_api_blueprint.route('/<id>',methods=["GET"])
def show(id):
    blog = Blog.get_or_none(Blog.title==id)
    blog_found = blog!=None
    result = jsonify({
        'status':blog_found,
        'data':blog.as_dict()
    })

    return result


@blogs_api_blueprint.route('/delete',methods=["POST"])
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



@blogs_api_blueprint.route("/edit",methods=["POST"])
@jwt_required
def edit():
    data = request.form
    target_blog = Blog.get_or_none(Blog.id==data['blog_id'])

    target_blog.title = data['blog_title']
    target_blog.d = data['blog_d']

    if target_blog.save():
        successfully_edited = True
    
    result = jsonify({
        'status' : successfully_edited,
        'data' : target_blog.as_dict()
    })

    return result