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
    test_db = client["edutask_test_db"]
    yield test_db
    client.drop_database("edutask_test_db")
    client.close()

@pytest.fixture
def sut(test_db):
    with patch('src.util.dao.pymongo.MongoClient') as mock_client:
        mock_client_instance = MagicMock()
        mock_client_instance.edutask = test_db
        mock_client.return_value = mock_client_instance
        dao_instance = DAO("video")
        yield dao_instance
        test_db.drop_collection("video")
