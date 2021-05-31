import unittest

from fastapi.testclient import TestClient

from niched.main import app

client = TestClient(app)


class ExampleClientTestCase(unittest.TestCase):
    def test_user_leo(self):
        response = client.get("/users/leo")
        assert response.status_code == 200
