import unittest

from fastapi.testclient import TestClient

from niched.main import app

client = TestClient(app)


class UserAuthenticationTestCase(unittest.TestCase):

    def test_login_successful(self):
        response = client.post("/auth/login",
                               headers={"Content-Type": "application/x-www-form-urlencoded",
                                        "accept": "application/json"},
                               data="username=test&password=test")
        assert response.status_code == 202
        res = response.json()
        assert res["token_type"] == "bearer"

    def test_login_unsuccessful_for_non_user(self):
        response = client.post("/auth/login",
                               headers={"Content-Type": "application/x-www-form-urlencoded",
                                        "accept": "application/json"},
                               data="username=non-existent&password=test")
        assert response.status_code == 401
