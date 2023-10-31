from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from .variables import PGDBHOSTPORT, PGDBNAME, PGDBPWD, PGDBUSERNAME, OPENAI_API_KEY, MIN_MOVIE_YEAR
from .logging_config import configure_logger
import string
import openai
import time
import pickle
from sys import getsizeof
from datetime import date

logger = configure_logger(__name__)


def get_movies_table_data():
    pg_engine = create_engine(f"postgresql://{PGDBUSERNAME}:{PGDBPWD}@{PGDBHOSTPORT}/{PGDBNAME}")
    Session = sessionmaker(bind=pg_engine)
    pg_session = Session()

    data = []
    current_year = date.today().year

    for year in range(MIN_MOVIE_YEAR, current_year + 1):
        result_proxy = pg_session.execute(text(f"SELECT * FROM movies WHERE is_vectorized = TRUE AND year = {year}"))
        column_names = result_proxy.keys()  
        queried_data = result_proxy.fetchall()
        
        data += [dict(zip(column_names, row)) for row in queried_data]

    pg_session.close()

    logger.info(f"Loaded data from DB into memory. # rows: {len(data)}, size: {round(getsizeof(data)/1000000,2)} MB")

    return data


def load_data_from_pickle(filename):
    try:
        with open(filename, 'rb') as file:
            data = pickle.load(file)
        return data
    
    except FileNotFoundError:
        return []


def preprocess_text(text):
    text = text.lower()  
    text = text.replace("\n", " ")
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text


def vectorize_text(text):  
    openai.api_key = OPENAI_API_KEY
    
    text = preprocess_text(text)
    try:
        embedding = list(openai.Embedding.create(input=[text], model="text-embedding-ada-002")["data"][0]["embedding"])

    except Exception as e:
        logger.info(f"Error vectorizing movie description:\n{e}")
        embedding = []

    return embedding


def get_movies_vector_matrix(movies_raw_data, include_genres):
    if include_genres: 
        return [row["vectorized_description"] for row in movies_raw_data]
    
    return [row["vectorized_description"][:-19] for row in movies_raw_data]



if __name__ == "__main__":
    start = time.perf_counter()
    get_movies_table_data()
    time_elapsed = (time.perf_counter() - start)    
    print("%5.1f secs" % (time_elapsed))

    start = time.perf_counter()
    vectorize_text("A movies about a happy dog")
    time_elapsed = (time.perf_counter() - start)    
    print("%5.1f secs" % (time_elapsed))