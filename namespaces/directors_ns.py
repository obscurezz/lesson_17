from flask import request, jsonify
from flask_restx import Namespace, Resource

from models import db, Director, DirectorSchema

directors_api = Namespace('directors', description='Director_API')

director_schema = DirectorSchema()


@directors_api.route('/')
class DirectorsView(Resource):
    """
    GET implements GET-method for directors
    """
    @staticmethod
    def get():
        all_directors = Director.query.all()
        try:
            return director_schema.dump(all_directors), 200
        except Exception as e:
            return jsonify({'exception': e}), 500


@directors_api.route('/<int:did>')
class DirectorView(Resource):
    """
    GET: implements GET-method for /directors/... where ... is ID of object
    POST: implements POST-method to add new object to database
    PUT: implements PUT-method to fully update object in database
    DELETE: implements DELETE-method to delete object from database
    """

    @staticmethod
    def get(did: int):
        exact_director = Director.query.get(did)
        try:
            return director_schema.dump(exact_director), 200
        except Exception as e:
            return jsonify({'exception': e}), 500

    @staticmethod
    def post():
        # response body of request
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
        # response body of request
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
