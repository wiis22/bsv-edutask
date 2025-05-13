import pytest
from pymongo import MongoClient
from src.util.dao import DAO
# from unittest.mock import patch
from dotenv import dotenv_values
from unittest.mock import MagicMock, patch

@pytest.fixture(scope="module")
def test_db():
    """Fixture to create a test database."""
    client = MongoClient(dotenv_values('.env').get('MONGO_URL'))
    yield client["edutask_test_db"]
    client.drop_database("edutask_test_db")
    client.close()

@pytest.fixture
def sut(test_db):
    test_collection_name = "video_test"

    test_db.drop_collection(test_collection_name)

    validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["url"],
            "properties": {
                "url": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                }
            }
        }
    }

    test_db.create_collection(test_collection_name, validator=validator)

    with patch('src.util.dao.pymongo.MongoClient') as mock_client:
        mock_client_instance = MagicMock()
        mock_client_instance.edutask = test_db
        mock_client.return_value = mock_client_instance
        yield DAO(test_collection_name)
        
        test_db.drop_collection(test_collection_name)