import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'a_very_secret_key_for_dev')  # Always use a strong secret key in production!
    # Common settings for all environments


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    PG_USER = os.getenv('PG_USER', 'dev_user')
    PG_PASSWORD = os.getenv('PG_PASSWORD', 'dev_password')
    PG_HOST = os.getenv('PG_HOST', 'localhost')
    PG_PORT = os.getenv('PG_PORT', '5432')
    PG_DATABASE = os.getenv('PG_DATABASE', 'dev_database')


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    PG_USER = os.getenv('PG_USER')  # Should be set in production environment variables
    PG_PASSWORD = os.getenv('PG_PASSWORD')
    PG_HOST = os.getenv('PG_HOST')
    PG_PORT = os.getenv('PG_PORT')
    PG_DATABASE = os.getenv('PG_DATABASE')

    # You might also have a single DATABASE_URI for SQLAlchemy
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    PG_USER = os.getenv('PG_TEST_USER', 'test_user')
    PG_PASSWORD = os.getenv('PG_TEST_PASSWORD', 'test_password')
    PG_HOST = os.getenv('PG_TEST_HOST', 'localhost')
    PG_PORT = os.getenv('PG_TEST_PORT', '5433')  # Use a different port for testing if possible
    PG_DATABASE = os.getenv('PG_TEST_DATABASE', 'test_database')


# A dictionary to easily select the configuration based on FLASK_ENV
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig  # Fallback
}
