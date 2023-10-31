import os
from dotenv import load_dotenv

load_dotenv()

THEMOVIEDB_API_ACCESS_TOKEN = os.getenv("THEMOVIEDB_API_ACCESS_TOKEN")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

PGDBUSERNAME = os.getenv("PGDBUSERNAME")

PGDBPWD = os.getenv("PGDBPWD")

PGDBHOSTPORT = os.getenv("PGDBHOSTPORT")

PGDBNAME = os.getenv("PGDBNAME")

SQL_QUERY_MOVIE_IDS_MAX_YEAR = os.getenv("SQL_QUERY_MOVIE_IDS_MAX_YEAR")
SQL_QUERY_MOVIES_TABLE = os.getenv("SQL_QUERY_MOVIES_TABLE")
SQL_QUERY_MOVIES_TABLE_MAX_YEAR = os.getenv("SQL_QUERY_MOVIES_TABLE_MAX_YEAR")

GENRES_DICT = {
    12: 'Adventure',
    14: 'Fantasy',
    16: 'Animation',
    18: 'Drama',
    27: 'Horror',
    28: 'Action',
    35: 'Comedy',
    36: 'History',
    37: 'Western',
    53: 'Thriller',
    80: 'Crime',
    99: 'Documentary',
    878: 'Science Fiction',
    9648: 'Mystery',
    10402: 'Music',
    10749: 'Romance',
    10751: 'Family',
    10752: 'War',
    10770: 'TV Movie'
    }

RAW_MOVIES_DATA_EXAMPLE =  [{
    'adult': False,
    'backdrop_path': '/J0XkW5toJLGEucm1pLDvTHXaKC.jpg',
    'genre_ids': [28, 18, 10752],
    'id': 1076487,
    'original_language': 'en',
    'original_title': 'Warhorse One',
    'overview': 'A gunned down Navy SEAL Master Chief must guide a child to '
                'safety through a gauntlet of hostile Taliban insurgents and '
                'survive the brutal Afghanistan wilderness.',
    'popularity': 634.402,
    'poster_path': '/jP2ik17jvKiV5sGEknMFbZv7WAe.jpg',
    'release_date': '2023-06-30',
    'title': 'Warhorse One',
    'video': False,
    'vote_average': 7.2,
    'vote_count': 159
    }]

MIN_MOVIE_YEAR = 1980
MAX_GETMOVIE_PAGE = 500
MAX_MOVIES_PER_PAGE = 20
MAX_MOVIES_TO_INSERT_PER_RUN = 6000