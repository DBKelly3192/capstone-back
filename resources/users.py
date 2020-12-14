from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
from playhouse.shortcuts import model_to_dict
import models

user = Blueprint('users','user')

@user.route('/create', methods=['POST'])
def create_user():
    payload = request.get_json()
    payload['email'] = payload['email'].lower()
    payload['emergencyEmail'] = payload['emergencyEmail']
    payload['emergencyFirst'] = payload['emergencyFirst']
    payload['emergencyLast'] = payload['emergencyLast']
    payload['first'] = payload['first']
    payload['last'] = payload['last']
    payload['lat'] = payload['lat']
    payload['lng'] = payload['lng']
    payload['photo'] = payload['photo']
    payload['username'] = payload['username'].lower()

    try:
        models.User.get(models.User.username == payload['username'])
        return jsonify(
            data={},
            message=f"The username, { payload['username'] }, already exists. Please select a different username.",
            status=401
        ), 401
    except models.DoesNotExist:
        try:
            models.User.get(models.User.email == payload['email'])
            return jsonify(
                data={},
                message=f"The email, { payload['email'] }, is already associated with an account. Please select a different email.",
                status=401
            ), 401
        except models.DoesNotExist:
            pw_hash = generate_password_hash(payload['password'])
            created_user = models.User.create(
                email=payload['email'],
                emergencyEmail = payload['emergencyEmail'],
                emergencyFirst = payload['emergencyFirst'],
                emergencyLast = payload['emergencyLast'],
                first = payload['first'],
                last = payload['last'],
                lat = payload['lat'],
                lng = payload['lng'],
                password=pw_hash,
                photo=payload['photo'],
                username=payload['username']
            )
            created_user_dict = model_to_dict(created_user)
            print(created_user_dict)
            created_user_dict.pop('password')

            return jsonify(
                data=created_user_dict,
                message=f"Successfully created user { created_user_dict['username'] }.",
                status=201
            ), 201

@user.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    payload['emailOrUsername'] = payload['emailOrUsername'].lower()

    try:
        user = models.User.get(models.User.username == payload['emailOrUsername'])
        return check_password(user, payload['password'])
    except models.DoesNotExist:
        try:
            user = models.User.get(models.User.email == payload['emailOrUsername'])
            return check_password(user, payload['password'])
        except models.DoesNotExist:
            return jsonify(
                data={},
                message="Email or password is incorrect. Please try again.",
                status=401
            ), 401

def check_password(user, password):
    user_dict = model_to_dict(user)
    password_is_good = check_password_hash(user_dict['password'], password)

    if(password_is_good):
        login_user(user)
        user_dict.pop('password')

        return jsonify(
            data=user_dict,
            message=f"Successfully logged in user {user_dict['username']}.",
            status=200
        ), 200
    else:
        return jsonify(
            data={},
            message="Username or password is incorrect. Please try again.",
            status=401
        ), 401


@user.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return jsonify(
        data={},
        message="Successfully logged out user.",
        status=200
    ), 200
