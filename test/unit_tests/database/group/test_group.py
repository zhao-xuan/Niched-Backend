import unittest
from unittest.mock import Mock
from datetime import datetime

from niched.database.group_utils import create_group, get_group, check_group_id_exist
from niched.models.schema.groups import GroupDataDB


class GroupMethodTestCase(unittest.TestCase):

    example_group = GroupDataDB(
            group_id      = "csgo",
            name          = "Counter Strike: Global Offsensive",
            description   = "CSGO players number 1!",
            image_url     = "http://media.steampowered.com/apps/csgo/blog/images/fb_image.png?v=6",
            creation_date = datetime.utcnow()
        )

    def test_create_groups_calls_insert_on_db(self):
        mock_client = Mock()
        create_group(mock_client, self.example_group)
        mock_client.insert_one.assert_called_once()

    def test_create_group_returns_true_when_new_group_created(self):
        mock_client = Mock()
        self.assertTrue(create_group(mock_client, self.example_group))

    def test_create_group_returns_false_when_new_group_create_failed(self):
        mock_client = Mock()
        mock_client.insert_one.side_effect = Exception("Cannot create user")
        self.assertFalse(create_group(mock_client, self.example_group))

    def test_get_group_queries_db(self):
        mock_client = Mock()
        get_group(mock_client, "")
        mock_client.find_one.assert_called()

    def test_get_user_returns_none_when_users_not_found(self):
        mock_client = Mock()
        mock_client.find_one.return_value = None
        self.assertIsNone(get_group(mock_client, ""))
