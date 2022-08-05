from flask import request, jsonify
from flask_restx import Namespace, Resource, fields

from models import db, Genre, GenreSchema

genres_api = Namespace('genres', description='Genre_API')

genre_schema = GenreSchema()


@genres_api.route('/<int:gid>')
class GenreView(Resource):
    @staticmethod
    def post():
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
