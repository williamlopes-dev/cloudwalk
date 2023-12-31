import sys
sys.path.append('../../cloudwalk')

from tests.base import Base

class TestRiskRecommendationEndpoint(Base):
    def setUp(self):
        super().setUp()
        
        self.account_id = 29744
        payload = {"account_id": self.account_id}
        response = self.client.post('/private/token', json=payload)
        access_token = response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        payload = {"username": "test", "password": "test"}
        response = self.client.post('/auth', json=payload, headers=headers)
        access_token = response.get_json()["access_token"]
        self.headers = {"Authorization": f"Bearer {access_token}"}

    def test_access_token_request_with_valid_params(self):
        payload = {"transaction_id" : 2342357, "merchant_id" : self.account_id, "user_id" : 97051, "card_number" : "434505******9116", "transaction_date" : "2019-12-01T23:16:32.812632", "transaction_amount" : 373.56, "device_id" : 285475}
        response = self.client.post('/risk/recommendation', json=payload, headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertIn(response.get_json()["recommendation"], ["approve", "deny"])

    def test_access_token_request_with_invalid_params(self):
        payload = {"transaction_id" : 2342357, "merchant_id" : self.account_id, "user_id" : 97051, "card_number" : "434505******9116", "transaction_date" : "2019-12-01T23:16:32.812632", "transaction_amount" : 373.56, "device_id" : 285475}
        for key in payload:
            self.app.extensions['limiter'].reset()
            custom_payload = payload.copy()

            custom_payload.pop(key)
            response = self.client.post('/risk/recommendation', json=custom_payload, headers=self.headers)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.get_json()["message"], f"Missing '{key}' field")

            custom_payload[key] = None
            response = self.client.post('/risk/recommendation', json=custom_payload, headers=self.headers)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.get_json()["message"], f"Missing '{key}' field")
    
    def test_access_token_request_with_invalid_account(self):
        payload = {"transaction_id" : 2342357, "merchant_id" : 123456, "user_id" : 97051, "card_number" : "434505******9116", "transaction_date" : "2019-12-01T23:16:32.812632", "transaction_amount" : 373.56, "device_id" : 285475}
        response = self.client.post('/risk/recommendation', json=payload, headers=self.headers)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json()["message"], "Invalid merchant")

    def test_access_token_request_without_params(self):
        payload = {}
        response = self.client.post('/risk/recommendation', json=payload, headers=self.headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["message"], "Missing 'transaction_id' field")

    def test_access_token_request_without_payload(self):
        payload = None
        response = self.client.post('/risk/recommendation', json=payload, headers=self.headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["message"], "Missing JSON in request")

    def test_access_token_request_without_access_token(self):
        payload = {"username": "william", "password": "will"}
        response = self.client.post('/risk/recommendation', json=payload)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json()["message"], "Missing Authorization Header")