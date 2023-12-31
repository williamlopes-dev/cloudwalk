import sys
sys.path.append('../../cloudwalk')

from tests.base import Base

class TestRateLimit(Base):
    def setUp(self):
        super().setUp()
        self.account_id = 29744

    def test_test_private_token_request_until_catch_rate_limit(self):
        i = 0
        while True:
            payload = {"account_id": self.account_id}
            response = self.client.post('/private/token', json=payload)

            if response.status_code == 429:
                break

            self.assertEqual(response.status_code, 201)
            self.assertIsNotNone(response.get_json()["access_token"])

            i += 1
        self.assertEqual(i, 60)

    def test_access_token_request_until_catch_rate_limit(self):
        payload = {"account_id": self.account_id}
        response = self.client.post('/private/token', json=payload)
        access_token = response.get_json()["access_token"]

        i = 0
        while True:
            payload = {"username": "test", "password": "test"}
            headers = {"Authorization": f"Bearer {access_token}"}
            response = self.client.post("/auth", json=payload, headers=headers)

            if response.status_code == 429:
                break

            self.assertEqual(response.status_code, 201)
            self.assertIsNotNone(response.get_json()["access_token"])

            i += 1
        self.assertEqual(i, 3)

    def test_fraud_prevention_request_until_catch_rate_limit(self):
        payload = {"account_id": self.account_id}
        response = self.client.post('/private/token', json=payload)
        access_token = response.get_json()["access_token"]

        payload = {"username": "test", "password": "test"}
        headers = {"Authorization": f"Bearer {access_token}"}
        response = self.client.post("/auth", json=payload, headers=headers)
        fresh_access_token = response.get_json()["access_token"]

        i = 0
        while True:
            payload = {"transaction_id" : 2342357, "merchant_id" : self.account_id, "user_id" : 97051, "card_number" : "434505******9116", "transaction_date" : "2019-12-01T23:16:32.812632", "transaction_amount" : 373.56, "device_id" : 285475}
            headers = {"Authorization": f"Bearer {fresh_access_token}"}
            response = self.client.post("/risk/recommendation", json=payload, headers=headers)

            if response.status_code == 429:
                break

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()["transaction_id"], payload["transaction_id"])
            self.assertIn(response.get_json()["recommendation"], ["approve", "deny"])

            i += 1
        self.assertEqual(i, 2)

