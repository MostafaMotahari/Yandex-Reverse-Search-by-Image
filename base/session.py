"""Session of postgresql"""

# Imports
from typing import Generator
import configparser

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Parsing bot configartion fot reading bot token
config = configparser.ConfigParser()
config.read("base/config.ini")

SQLALCHEMY_DATABASE_URL = config["database"]["postgresql_url"]
engine = create_engine(SQLALCHEMY_DATABASE_URL)
local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator:
    try:
        db = local_session()
        yield db
    finally:
        db.close()


# Temporary databsae
TEMP_DATA = []
