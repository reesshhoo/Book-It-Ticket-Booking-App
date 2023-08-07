import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
    SMTP_SERVER_HOST = "localhost"
    SMTP_SERVER_PORT = 1025
    SENDER_ADDRESS = ""
    SENDER_PASSWORD = ""
    REDIS_URL = "redis://localhost:6379"
    CACHE_TYPE = "redis"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_DEFAULT_TIMEOUT = 300


class LocalDevelopmentConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir, "../instance")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "database.sqlite3")
    DEBUG = True
    SECRET_KEY = "your-secret-key"  # Replace with your actual secret key
    JWT_SECRET_KEY = "your-jwt-secret-key"  # Replace with your actual JWT secret key
    # SECURITY_PASSWORD_HASH = "sha256_crypt"  # Use 'sha256_crypt' for werkzeug.security.generate_password_hash
    # SECURITY_PASSWORD_SALT = "really-super-secret"
    # SECURITY_REGISTERABLE = True
    # SECURITY_SEND_REGISTER_EMAIL = False
    # SECURITY_UNAUTHORIZED_VIEW = None
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
    SMTP_SERVER_HOST = "localhost"
    SMTP_SERVER_PORT = 1025
    SENDER_ADDRESS = ""
    SENDER_PASSWORD = ""
    REDIS_URL = "redis://localhost:6379"
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_DEFAULT_TIMEOUT = 300
