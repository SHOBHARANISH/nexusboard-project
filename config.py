import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Default configuration for NotifyNet app."""
    SECRET_KEY = 'your-secret-key'  # You can change this later
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'notifynet.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    """Configuration for testing."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
