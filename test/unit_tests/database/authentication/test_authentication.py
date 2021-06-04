import unittest
from unittest.mock import Mock

from niched.database.authentication import create_user, get_user_login_details
from niched.models.schema.users import UserDetailsDB


class UsersAuthTestCase(unittest.TestCase):

    def test_create_user_calls_insert_on_db(self):
        mock_client = Mock()

        user = UserDetailsDB(username="test", password="test")
        create_user(mock_client, user)
        mock_client.insert_one.assert_called_once()

    def test_create_user_returns_true_when_new_user_created(self):
        mock_client = Mock()

        user = UserDetailsDB(username="test", password="test")
        self.assertTrue(create_user(mock_client, user))

    def test_create_user_returns_false_when_new_user_create_failed(self):
        mock_client = Mock()
        mock_client.insert_one.side_effect = Exception("Cannot create user")

        user = UserDetailsDB(username="test", password="test")
        self.assertFalse(create_user(mock_client, user))

    def test_get_user_queries_db(self):
        mock_client = Mock()

        get_user_login_details(mock_client, "")
        mock_client.find_one.assert_called()

    def test_get_user_returns_none_when_users_not_found(self):
        mock_client = Mock()
        mock_client.find_one.return_value = None

        self.assertIsNone(get_user_login_details(mock_client, ""))
