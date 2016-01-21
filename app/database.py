from sqlalchemy import (
    create_engine,
    MetaData
)
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# create database engine
engine = create_engine('sqllite:///tmp/test.db', convert_unicode=True)

# create database session
db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine
))

# get database metadata
metadata = MetaData(bind=engine)

# configure declarative base
Base = declarative_base()
Base.query = db_session.query_property()


# initialize database
def init_db():
    import users.models
    import sites.models
    import pages.models
    import schedules.models
    metadata.create_all(bind=engine)
