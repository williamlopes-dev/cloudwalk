import sys
sys.path.append('../../cloudwalk')

from tests.base import Base

class AccessTokenParamsTests(Base):
    def setUp(self):
        super().setUp()
        self.account_id = 29744

    def test_private_token_request_with_valid_params(self):
        payload = {"account_id": self.account_id}
        response = self.client.post('/private/token', json=payload)

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.get_json()["access_token"])

    def test_private_token_request_with_invalid_params(self):
        payload = {"account_id": 999999}
        response = self.client.post('/private/token', json=payload)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json()["message"], "Invalid account")

    def test_private_token_request_without_params(self):
        payload = {}
        response = self.client.post('/private/token', json=payload)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["message"], "Missing 'account_id' parameter")

    def test_private_token_request_without_payload(self):
        payload = None
        response = self.client.post('/private/token', json=payload)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["message"], "Missing JSON in request")