import pytest
import unittest.mock as mock

from src.controllers.usercontroller import UserController
from src.util.dao import DAO

@pytest.fixture
def dao_mock():
    """Fixture to create a mock DAO object."""
    dao = mock.MagicMock(DAO)
    return dao

@pytest.fixture
def user_controller(dao_mock):
    """Fixture to create a UserController object with the mocked DAO."""
    return UserController(dao=dao_mock)

def test_valid_email_one_user_found(user_controller, dao_mock):
    """Test case for a valid email with one user found."""
    user = {'email': 'test_1@example.com'}
    dao_mock.find.return_value = [user]
    result = user_controller.get_user_by_email('test_1@example.com')
    assert result == user

def test_valid_email_multiple_users_found(user_controller, dao_mock):
    """Test case for a valid email with multiple users found."""
    users = [
        {'email': 'test_2@example.com', 'id': 1},
        {'email': 'test_2@example.com', 'id': 2},
    ]
    dao_mock.find.return_value = users

    # Capture the print output
    with mock.patch('builtins.print') as mock_print:
        result = user_controller.get_user_by_email('test_2@example.com')

        # Check that the print function was called with the expected message
        mock_print.assert_called_once_with('Error: more than one user found with mail test_2@example.com')

        assert result == users[0]

def test_valid_email_no_user_found(user_controller, dao_mock):
    """Test case for a valid email with no user found."""
    dao_mock.find.return_value = []
    result = user_controller.get_user_by_email('test_3@example.com')
    
    dao_mock.find.assert_called_once_with({'email': 'test_3@example.com'})
    assert result is None

def test_database_error(user_controller, dao_mock):
    """Test case for a database error."""
    dao_mock.find.side_effect = Exception("Database error")
    
    with pytest.raises(Exception):
        user_controller.get_user_by_email('test_4@example.com')

@pytest.mark.parametrize("invalid_email", [
    "example.com",          #no @
    "test@",                #no domain
    "",                     #empty string
    " test@example.com.",   #leading white space
])
def test_invalid_email(user_controller, invalid_email):
    """Test case for invalid email addresses."""
    with pytest.raises(ValueError):
        user_controller.get_user_by_email(invalid_email)


