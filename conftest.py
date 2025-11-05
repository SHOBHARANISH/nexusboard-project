import os
import sys
import pytest

# Make sure the project root directory is in Python's path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app as flask_app   # Import your Flask app directly

@pytest.fixture(scope='session')
def app():
    """Create a Flask app instance for testing."""
    flask_app.config.update({
        "TESTING": True,
    })

    # Return app instance for tests
    yield flask_app


@pytest.fixture(scope='function')
def client(app):
    """Flask test client."""
    return app.test_client()
