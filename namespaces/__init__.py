from flask_restx import Api

from .movie_ns import movies_api
from .directors_ns import directors_api
from .genres_ns import genres_api

api = Api(
    title='Lesson17_API',
    version='1.0',
    description='All namespaces of project into one API'
)

api.add_namespace(movies_api)
api.add_namespace(directors_api)
api.add_namespace(genres_api)
