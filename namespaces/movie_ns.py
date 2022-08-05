from flask import request, jsonify
from flask_restx import Namespace, Resource

from models import db, Movie, MovieSchema

movies_api = Namespace('movies', description='Movie_API')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movies_api.route('/')
class MoviesView(Resource):
    """
    GET: implements GET-method for movies
    /movies/?page=... - pagination by 3
    /movies/?genre_id=... - finds objects by genre_id
    /movies/?director_id=... - finds objects by director_id
    /movies/?director_id=...&genre_id=... - finds objects by both genre_id and director_id
    """
    @staticmethod
    def get():
        # pagination query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 3, type=int)

        # lateral keys query parameters
        genre = request.args.get('genre_id')
        director = request.args.get('director_id')

        # queries for lateral keys
        genre_movies = Movie.query.filter(Movie.genre_id == genre)
        director_movies = Movie.query.filter(Movie.director_id == director)
        both_movies = Movie.query.filter(Movie.genre_id == genre, Movie.director_id == director)

        # full query
        all_movies = Movie.query
        # choosing what result to return
        if None not in (genre, director):
            result_query = both_movies
        elif genre is not None:
            result_query = genre_movies
        elif director is not None:
            result_query = director_movies
        else:
            result_query = all_movies
        # paginate result
        pagination = result_query.paginate(page, per_page).items

        try:
            return movies_schema.dump(pagination), 200
        except Exception as e:
            return jsonify({'exception': e}), 500


@movies_api.route('/<int:mid>')
class MovieView(Resource):
    """
    GET: implements GET-method for /movies/... where ... is ID of object
    """
    @staticmethod
    def get(mid: int):
        # getting exact object by primary key
        exact_movie = db.session.query(Movie).get(mid)
        try:
            return movie_schema.dump(exact_movie), 200
        except Exception as e:
            return jsonify({'exception': e}), 500
