import string
import numpy as np
import tiktoken
import openai
import traceback
from pprint import pprint
from .variables import OPENAI_API_KEY, GENRES_DICT, RAW_MOVIES_DATA_EXAMPLE
from .logging_config import configure_logger


logger = configure_logger(__name__)


def preprocess_text(text):
    text = text.lower()  
    text = text.replace("\n", " ")
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text


def num_tokens_from_string(string):
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(string))
    return num_tokens


def vectorize_text_with_categories(text, categories, all_categories):
    openai.api_key = OPENAI_API_KEY
    
    text = preprocess_text(text)
    logger.debug(num_tokens_from_string(text))

    try:
        embeddings = openai.Embedding.create(input=[text], model="text-embedding-ada-002")["data"][0]["embedding"] 
        genre_vector = [1 if cat in categories else 0 for cat in all_categories] 
        combined_vector = np.concatenate([embeddings, genre_vector], axis=0).tolist()

    except Exception as e:
        logger.info(f"Error vectorizing movie description:\n{e}")
        traceback_str = traceback.format_exc()
        logger.debug(traceback_str)

        combined_vector = []

    return combined_vector


def transform_movie(row, genres_dict):
    logger.info(f"Transforming movie: {row['title']}")

    movie = {
        "id": row["id"],
        "name": row["title"],
        "description": row["overview"],
        "vote": float(row["vote_average"]),
        "vote_count": int(row["vote_count"]),
        "year": int(row["release_date"][:4]),
        "genres": ", ".join([genres_dict.get(i, "Unknown Genre") for i in row["genre_ids"]]),
        "language": row["original_language"],
        "vectorized_description": vectorize_text_with_categories(row["overview"], row["genre_ids"], genres_dict.keys())
    }
    movie["is_vectorized"] =  True if movie["vectorized_description"] else False
    return movie


def transform_movies_data(raw_movies_data, genres_dict):
    movies_data_list = [transform_movie(row, genres_dict) for row in raw_movies_data]
    return movies_data_list



if __name__ == "__main__":
    
    movies_data_list = transform_movies_data(RAW_MOVIES_DATA_EXAMPLE, GENRES_DICT)
    for movie_data in movies_data_list:
        movie_data["vectorized_description"] = movie_data["vectorized_description"][:20]
    pprint(movies_data_list)