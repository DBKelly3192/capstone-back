from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict
import models

sos = Blueprint('soss', 'sos')

@sos.route('/my', methods = ['GET'])
def my_soss():
    try:
        soss = [model_to_dict(sos) for sos in current_user.soss]
        print(f"LIST OF SOS. { soss }")

        return jsonify(
            data = soss,
            status = { "code": 201, "message": "success" }
        )

    except models.DoesNotExist:
        return jsonify(
            data = {},
            status = { "code": 401, "message": "Error getting Resources" }
        )

@sos.route('/<id>', methods = ["GET"])
def one_sos(id):
    sos = models.SOS.get_by_id(id)
    print(sos)
    return jsonify(
        data = model_to_dict(sos),
        status = { "code": 200, "message": "Success" }
    )

@sos.route('/create', methods = ["POST"])
def create_sos():
    print('In the create route')
    try:
        payload = request.get_json()
        print(f'This is the payload { payload }')
        created_sos = models.SOS.create(
            activity = payload['activity'],
            description = payload['description'],
            finish = payload['finish'],
            location = payload['location'],
            start = payload['start'],
            user = current_user.id
        )
        print(f'This is the created model { created_sos }')
        sos_dict = model_to_dict(created_sos)

        return jsonify(
            data = sos_dict,
            status = { "code": 201, "message": "Success" }
        )
    except:
        return jsonify(status={ "code": 400, "message": "Not Successful" })

@sos.route('/<id>', methods = ["PUT"])
def update_sos(id):
    payload = request.get_json()
    query = models.SOS.update(**payload).where(models.SOS.id == id)
    query.execute()
    sos = model_to_dict(models.SOS.get_by_id(id))

    return jsonify(
        data = sos,
        status = { "code": 200, "message": "Success" }
    )

@sos.route('/<id>', methods = ["DELETE"])
def delete_sos(id):
    delete_query = models.SOS.delete().where(models.SOS.id == id)
    num_of_rows_deleted = delete_query.execute()
    return jsonify(
        data = {},
        message = f"SOS with id { id } deleted, { num_of_rows_deleted } row total.",
        status={ "code": 200 }
    )
