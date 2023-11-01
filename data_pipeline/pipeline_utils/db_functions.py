from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import inspect, insert, text
from .logging_config import configure_logger


logger = configure_logger(__name__)

# Define tables

Base = declarative_base()

class MoviesTable(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    vote = Column(Float)
    vote_count = Column(Integer)
    year = Column(Integer)
    genres = Column(String)
    language = Column(String)
    vectorized_description = Column(JSONB)
    is_vectorized = Column(Boolean)



# Define functions

def create_movies_table_if_not_exists(engine):
    inspector = inspect(engine)
    if "movies" not in inspector.get_table_names():
        Base.metadata.create_all(engine)
        logger.info("Movies Table has been created.")


def batch_insert_movies_data(session, movie_data_list):
    ins = insert(MoviesTable).values(movie_data_list)
    session.execute(ins)
    session.commit()


def query_db(session, query):
    result_proxy = session.execute(text(query))
    column_names = result_proxy.keys()  # Get column names from the result
    queried_data = result_proxy.fetchall()
    
    result_list = [dict(zip(column_names, row)) for row in queried_data]
    return result_list



if __name__ == "__main__":
    logger.info("TEST")