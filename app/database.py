from sqlalchemy import (
    create_engine,
    MetaData
)
from sqlalchemy.orm import scoped_session, sessionmaker


# create database engine
engine = create_engine('sqllite:///tmp/test.db', convert_unicode=True)

# get database metadata
metadata = MetaData(bind=engine)

# create database session
db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine
))


# initialize database
def init_db():
    metadata.create_all(bind=engine)
