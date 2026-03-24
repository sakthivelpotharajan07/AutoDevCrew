from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db = SQLAlchemy()

Base = declarative_base()

def create_database_engine():
    database_url = current_app.config['DATABASE_URL']
    engine = create_engine(database_url)
    return engine

def create_session():
    engine = create_database_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def create_tables():
    engine = create_database_engine()
    Base.metadata.create_all(engine)

def get_db_session():
    session = create_session()
    return session