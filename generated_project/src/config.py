Python

class Config:
    FLASK_APP = 'app'
    FLASK_ENV = 'development'
    FLASK_DEBUG = True
    SECRET_KEY = 'secret_key_here'

class DatabaseConfig:
    DB_HOST = 'localhost'
    DB_PORT = 5432
    DB_NAME = 'cake_ordering'
    DB_USER = 'postgres'
    DB_PASSWORD = 'password_here'

    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Configurations:
    DEFAULT = Config
    DB = DatabaseConfig