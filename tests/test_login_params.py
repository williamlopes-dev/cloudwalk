import sys
sys.path.append('../../cloudwalk')

from tests.base import Base

class LoginParamsTests(Base):
    def setUp(self):
        super().setUp()
        
        account_id = 29744
        payload = {"account_id": account_id}
        response = self.client.post('/private/token', json=payload)
        access_token = response.get_json()["access_token"]
        self.headers = {"Authorization": f"Bearer {access_token}"}

    def test_login_request_with_valid_params(self):
        payload = {"username": "test", "password": "test"}
        response = self.client.post('/login', json=payload, headers=self.headers)

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.get_json()["access_token"])

    def test_login_request_with_invalid_params(self):
        payload = {"username": "william", "password": "will"}
        response = self.client.post('/login', json=payload, headers=self.headers)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json()["message"], "Invalid username or password")

    def test_login_request_without_params(self):
        payload = {}
        response = self.client.post('/login', json=payload, headers=self.headers)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json()["message"], "Invalid username or password")

    def test_login_request_without_payload(self):
        payload = None
        response = self.client.post('/login', json=payload, headers=self.headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["message"], "Missing JSON in request")

    def test_login_request_without_access_token(self):
        payload = {"username": "william", "password": "will"}
        response = self.client.post('/login', json=payload)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json()["message"], "Missing Authorization Header")