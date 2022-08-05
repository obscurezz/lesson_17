from flask import request, jsonify
from flask_restx import Namespace, Resource

from models import db, Movie, MovieSchema

movies_api = Namespace('movies', description='Movie_API')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movies_api.route('/<int:page>')
class MoviesView(Resource):
    @staticmethod
    def get(page=1):
        genre = request.args.get('genre_id')
        director = request.args.get('director_id')

        all_movies = db.session.query(Movie).paginate(page, 5, False).items

        genre_movies = db.session.query(Movie).filter(Movie.genre_id == genre)
        director_movies = db.session.query(Movie).filter(Movie.director_id == director)

        both_movies = db.session.query(Movie).filter(Movie.genre_id == genre, Movie.director_id == director)

        try:
            if None not in (genre, director):
                return movies_schema.dump(both_movies), 200
            elif genre is not None:
                return movies_schema.dump(genre_movies), 200
            elif director is not None:
                return movies_schema.dump(director_movies), 200
            else:
                return movies_schema.dump(all_movies), 200
        except Exception as e:
            return jsonify({'exception': e}), 500


@movies_api.route('/find/<int:mid>')
class MovieView(Resource):
    @staticmethod
    def get(mid: int):
        exact_movie = db.session.query(Movie).get(mid)
        try:
            return movie_schema.dump(exact_movie), 200
        except Exception as e:
            return jsonify({'exception': e}), 500
