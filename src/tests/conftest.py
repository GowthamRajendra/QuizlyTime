import pytest
from flask import Flask
from mongoengine import connect, disconnect
from mongomock import MongoClient
import mongomock

from src.app import create_app

@pytest.fixture
def app():
    # Set up the Flask app with mock database
    app = create_app()

    # Disconnect any existing database connections
    disconnect()

    # Connect to a mock database
    connect('QuizAppDB', mongo_client_class=MongoClient, uuidRepresentation="standard")

    # Yield the app for testing
    yield app

    # Disconnect the mock database after testing
    disconnect()

@pytest.fixture
def client(app):
    # Create a test client
    with app.test_client() as client:
        yield client