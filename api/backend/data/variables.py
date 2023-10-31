import os
from dotenv import load_dotenv

load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

PGDBUSERNAME = os.getenv("PGDBUSERNAME")

PGDBPWD = os.getenv("PGDBPWD")

PGDBHOSTPORT = os.getenv("PGDBHOSTPORT")

PGDBNAME = os.getenv("PGDBNAME")

MIN_MOVIE_YEAR = 1980

NODES_DATA_COLUMNS = ["id", "name", "description", "vote", "vote_count", "year", "genres", "language"]

MIN_COS_SIM_SCORE = 0.8