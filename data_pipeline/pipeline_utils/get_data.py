import requests
from pprint import pprint
from .logging_config import configure_logger
from .variables import THEMOVIEDB_API_ACCESS_TOKEN


logger = configure_logger(__name__)


def get_movies_data(page,primary_release_year,include_adult="false",language="en-US",with_original_language="en",vote_average_gte=5.5,vote_count_gte=100.0):
    URL = "https://api.themoviedb.org/3/discover/movie"
    headers = {
        "accept":"application/json",
        "Authorization":f"Bearer {THEMOVIEDB_API_ACCESS_TOKEN}"
    }
    params = {
        "language":language,
        "with_original_language":with_original_language,
        "page":page,
        "include_adult":include_adult,
        "vote_average.gte":vote_average_gte,
        "vote_count.gte":vote_count_gte,
        "primary_release_year":primary_release_year
    }
    try:
        logger.info(f"Getting movies data for year - {primary_release_year}, for page - {page}")
        response_dict = requests.get(URL, headers=headers, params=params).json()

        if "error" in response_dict:
            error_msg = response_dict["error"]
            raise Exception(error_msg)

        return response_dict["results"]
    except Exception as e:
        logger.info(f"Error for year - {primary_release_year}, for page - {page}:\n{e}")
        return []


def get_genres_data():
    URL = "https://api.themoviedb.org/3/genre/movie/list?language=en"
    headers = {
        "accept":"application/json",
        "Authorization":f"Bearer {THEMOVIEDB_API_ACCESS_TOKEN}"
    }
    try:
        logger.info(f"Getting genres data")
        response_dict = requests.get(URL, headers=headers).json()

        if "error" in response_dict:
            error_msg = response_dict["error"]
            raise Exception(error_msg)

        genres_dict = {i["id"]:i["name"] for i in response_dict["genres"]}
        return genres_dict
    except Exception as e:
        logger.info(f"Error on getting genres data:\n{e}")
        return []
    


if __name__ == "__main__":
    
    pprint(get_movies_data(page=1, primary_release_year=2023))
    pprint(get_genres_data())