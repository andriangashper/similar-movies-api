from datetime import date
import traceback
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_pipeline.pipeline_utils.logging_config import configure_logger
from data_pipeline.pipeline_utils import get_data
from data_pipeline.pipeline_utils import transform_data
from data_pipeline.pipeline_utils import db_functions
from data_pipeline.pipeline_utils.variables import \
    PGDBNAME, PGDBPWD, PGDBUSERNAME, PGDBHOSTPORT, \
    SQL_QUERY_MOVIE_IDS_MAX_YEAR, \
    GENRES_DICT, \
    MAX_MOVIES_TO_INSERT_PER_RUN, \
    MIN_MOVIE_YEAR, \
    MAX_GETMOVIE_PAGE

logger = configure_logger(__name__)


def update_movies_table_pipeline():
    ''' 
    Updating movies table. 
    The pipeline will read from the movies table, existing movie ids, from the max year.
    Then from and including that year until and including the present year
    it will get all the movies and will insert the new ones.
    A page length variable will be used to start retrieving later movies from a given year.
    This will ensure we are not reading too much unnecessary data, 
    will update the database with the most recent movies.
    P.S. For now, it does not adjust the changes to existing movies.
    NOTE: The pipeline has a limit of movies to add per run.
    '''


    pg_engine = create_engine(f"postgresql://{PGDBUSERNAME}:{PGDBPWD}@{PGDBHOSTPORT}/{PGDBNAME}")
    db_functions.create_movies_table_if_not_exists(pg_engine)
    
    Session = sessionmaker(bind=pg_engine)
    pg_session = Session()
    logger.info("Session created")

    try:  # try except here is used to close the database session in case of an error

        max_year_movies = db_functions.query_db(pg_session, SQL_QUERY_MOVIE_IDS_MAX_YEAR)
        max_year_movie_ids = [id_dict["id"] for id_dict in max_year_movies]

        max_year = max_year_movies[0]["year"] if max_year_movies else MIN_MOVIE_YEAR
        current_year = date.today().year

        len_max_year_movie_ids = len(max_year_movie_ids)
        logger.info(f"{len_max_year_movie_ids} movies found in Database for max year {max_year}")

        page = 1 
        total_movies_inserted = 0

        for year in range(max_year, current_year+1):

            if total_movies_inserted > MAX_MOVIES_TO_INSERT_PER_RUN:
                break

            movies_inserted = 0
            while page <= MAX_GETMOVIE_PAGE and total_movies_inserted <= MAX_MOVIES_TO_INSERT_PER_RUN:

                temp_movies_data = get_data.get_movies_data(page, year)
                logger.info(f"{len(temp_movies_data)} movies extracted from TMDB API")

                if temp_movies_data:
                    filtered_temp_movies_data = [movie for movie in temp_movies_data if movie["id"] not in max_year_movie_ids]

                    if filtered_temp_movies_data:
                        movies_data_to_insert = transform_data.transform_movies_data(filtered_temp_movies_data, GENRES_DICT)
                        db_functions.batch_insert_movies_data(pg_session, movies_data_to_insert)

                        total_movies_inserted += len(movies_data_to_insert)
                        movies_inserted += len(movies_data_to_insert)
                        logger.info(f"{len(movies_data_to_insert)} movies have been inserted into the Database")
                    
                    page += 1
                else:
                    page += 1
                    break

            logger.info(f"Movies inserted: {movies_inserted}, for year: {year}, max page: {page-1}")
            logger.info(f"Total Movies inserted: {total_movies_inserted}")
            page = 1

    except Exception as e:
        logger.info(e)
        traceback_str = traceback.format_exc()
        logger.info(traceback_str)

    pg_session.close()
    logger.info("Session closed")



if __name__ == "__main__":
    update_movies_table_pipeline()