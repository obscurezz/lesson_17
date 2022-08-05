from flask import request, jsonify
from flask_restx import Namespace, Resource, fields

from models import db, Director, DirectorSchema

directors_api = Namespace('directors', description='Director_API')

director_schema = DirectorSchema()


@directors_api.route('/<int:did>')
class DirectorView(Resource):
    @staticmethod
    def post():
        json_request: dict = request.json
        new_director = Director(**json_request)

        db.session.add(new_director)
        try:
            db.session.commit()
            return "", 201
        except Exception as e:
            return jsonify({'error': e}), 500

    @staticmethod
    def put(did: int):
        json_request: dict = request.json
        exact_director = db.session.query(Director).get(did)

        for k in json_request:
            setattr(exact_director, k, json_request[k])

        db.session.add(exact_director)
        try:
            db.session.commit()
            return "", 204
        except Exception as e:
            return jsonify({'error': e}), 500

    @staticmethod
    def delete(did: int):
        exact_director = db.session.query(Director).get(did)

        db.session.delete(exact_director)
        try:
            db.session.commit()
            return "", 204
        except Exception as e:
            return jsonify({'error': e}), 500
