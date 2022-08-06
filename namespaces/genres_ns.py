from flask import request, jsonify
from flask_restx import Namespace, Resource

from models import db, Genre, GenreSchema

genres_api = Namespace('genres', description='Genre_API')

genre_schema = GenreSchema()


@genres_api.route('/')
class GenresView(Resource):
    """
    GET implements GET-method for directors
    """

    @staticmethod
    def get():
        all_genres = Genre.query.all()
        try:
            return genre_schema.dump(all_genres), 200
        except Exception as e:
            return jsonify({'exception': e}), 500


@genres_api.route('/<int:gid>')
class GenreView(Resource):
    """
    GET: implements GET-method for /genres/... where ... is ID of object
    POST: implements POST-method to add new object to database
    PUT: implements PUT-method to fully update object in database
    DELETE: implements DELETE-method to delete object from database
    """

    @staticmethod
    def get(gid: int):
        exact_genre = Genre.query.get(gid)
        try:
            return genre_schema.dump(exact_genre), 200
        except Exception as e:
            return jsonify({'exception': e}), 500

    @staticmethod
    def post():
        # response body of request
        json_request: dict = request.json
        new_genre = Genre(**json_request)

        db.session.add(new_genre)
        try:
            db.session.commit()
            return "", 201
        except Exception as e:
            return jsonify({'error': e}), 500

    @staticmethod
    def put(did: int):
        # response body of request
        json_request: dict = request.json
        exact_genre = db.session.query(Genre).get(did)

        for k in json_request:
            setattr(exact_genre, k, json_request[k])

        db.session.add(exact_genre)
        try:
            db.session.commit()
            return "", 204
        except Exception as e:
            return jsonify({'error': e}), 500

    @staticmethod
    def delete(did: int):
        exact_genre = db.session.query(Genre).get(did)

        db.session.delete(exact_genre)
        try:
            db.session.commit()
            return "", 204
        except Exception as e:
            return jsonify({'error': e}), 500
