from flask_restx.reqparse import RequestParser

director_parser: RequestParser = RequestParser()
director_parser.add_argument(name='director_id', type=int, required=False, nullable=False)

genre_parser: RequestParser = RequestParser()
genre_parser.add_argument(name='genre_id', type=int, required=False, nullable=False)
