from flask import request, jsonify
from flask_restx import Namespace, Resource

from config import PaginationConfig
from models import db, Movie, MovieSchema
from parsers import director_parser, genre_parser

movies_api = Namespace('movies', description='Movie_API')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movies_api.route('/')
class MoviesView(Resource):
    """
    GET: implements GET-method for movies
    /movies/?genre_id=... - finds objects by genre_id
    /movies/?director_id=... - finds objects by director_id
    /movies/?director_id=...&genre_id=... - finds objects by both genre_id and director_id
    """

    @staticmethod
    def get():
        # pagination query parameters
        page = PaginationConfig.PAGE
        per_page = PaginationConfig.PER_PAGE

        # lateral keys query parameters
        lateral_parser = {k: v for k, v in {**director_parser.parse_args(), **genre_parser.parse_args()}.items() if
                          v is not None}

        # base query
        result_query = Movie.query.filter_by(**lateral_parser)
        # paginate result
        pagination = result_query.paginate(page=page, per_page=per_page).items

        try:
            return movies_schema.dump(pagination), 200
        except Exception as e:
            return jsonify({'exception': e}), 500


@movies_api.route('/<int:mid>')
class MovieView(Resource):
    """
    GET: implements GET-method for /movies/... where ... is ID of object
    POST: implements POST-method to add new object to database
    PUT: implements PUT-method to fully update object in database
    DELETE: implements DELETE-method to delete object from database
    """

    @staticmethod
    def get(mid: int):
        # getting exact object by primary key
        exact_movie = db.session.query(Movie).get(mid)
        try:
            return movie_schema.dump(exact_movie), 200
        except Exception as e:
            return jsonify({'exception': e}), 500

    @staticmethod
    def post():
        # response body of request
        json_request: dict = request.json
        new_movie = Movie(**json_request)

        db.session.add(new_movie)
        try:
            db.session.commit()
            return "", 201
        except Exception as e:
            return jsonify({'error': e}), 500

    @staticmethod
    def put(mid: int):
        # response body of request
        json_request: dict = request.json
        exact_movie = db.session.query(Movie).get(mid)

        for k in json_request:
            setattr(exact_movie, k, json_request[k])

        db.session.add(exact_movie)
        try:
            db.session.commit()
            return "", 204
        except Exception as e:
            return jsonify({'error': e}), 500

    @staticmethod
    def delete(mid: int):
        exact_movie = db.session.query(Movie).get(mid)

        db.session.delete(exact_movie)
        try:
            db.session.commit()
            return "", 204
        except Exception as e:
            return jsonify({'error': e}), 500
