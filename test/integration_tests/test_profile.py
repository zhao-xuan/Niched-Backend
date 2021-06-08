import unittest

from fastapi.testclient import TestClient

from niched.main import app

client = TestClient(app)


class ProfileTestCase(unittest.TestCase):

    def test_get_user_profile_successful(self):
        response = client.get("/profile/alice")
        assert response.status_code == 200


    # Integration test to be added for groups after we complete all group functionality
    #     i.e. add