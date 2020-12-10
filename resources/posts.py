from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict
import models

post = Blueprint('posts', 'post')

@post.route('/all', methods = ['GET'])
def all_posts():
    try:
        all_posts = [model_to_dict(post) for post in models.Post]

        return jsonify(
            data = all_posts,
            status = { "code": 201, "message": "success" }
        )

    except models.DoesNotExist:
        return jsonify(
            data = {},
            status = { "code": 401, "message": "Error getting Resources" }
        )

@post.route('/my', methods = ['GET'])
def my_posts():
    try:
        posts = [model_to_dict(post) for post in current_user.posts]
        print(f"LIST OF POSTS. { posts }")

        return jsonify(
            data = posts,
            status = { "code": 201, "message": "success" }
        )

    except models.DoesNotExist:
        return jsonify(
            data={},
            status={ "code": 401, "message": "Error getting Resources" }
        )

@post.route('/<id>', methods = ["GET"])
def one_post(id):
    post = models.Post.get_by_id(id)

    return jsonify(
        data = model_to_dict(post),
        status = { "code": 200, "message": "Success" }
    )

@post.route('/create', methods = ["POST"])
def create_post():
    try:
        payload = request.get_json()
        created_post = models.Post.create(
            activity = payload['activity'],
            description = payload['description'],
            location = payload['location'],
            user = current_user.id
        )
        post_dict = model_to_dict(created_post)

        return jsonify(
            data = post_dict,
            status = { "code": 201, "message": "Success" }
        )
    except:
        return jsonify(status={ "code": 400, "message": "Not Successful" })

@post.route('/<id>', methods = ["PUT"])
def update_post(id):
    payload = request.get_json()
    query = models.Post.update(**payload).where(models.Post.id == id)
    query.execute()
    post = model_to_dict(models.Post.get_by_id(id))

    return jsonify(
        data = post,
        status = { "code": 200, "message": "Success" }
    )

@post.route('/<id>', methods = ["DELETE"])
def delete_post(id):
    delete_query = models.Post.delete().where(models.Post.id == id)
    num_of_rows_deleted = delete_query.execute()
    return jsonify(
        data = {},
        message = f"Post with id { id } deleted, { num_of_rows_deleted } row total.",
        status={ "code": 200 }
    )
