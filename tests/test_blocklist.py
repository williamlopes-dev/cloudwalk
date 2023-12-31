import sys
sys.path.append('../../cloudwalk')

from tests.base import Base

from fraud_prevention.database.blocklist import Blocklist

class TestBlocklist(Base):
    def setUp(self):
        super().setUp()
        Blocklist.clear()
        self.account_id = 29744

        payload = {"account_id": self.account_id}
        response = self.client.post('/private/token', json=payload)
        self.access_token = response.get_json()["access_token"]

    def test_access_token_request_with_empty_blocklist(self):
        payload = {"username": "test", "password": "test"}
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = self.client.post("/auth", json=payload, headers=headers)

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.get_json()["access_token"])

    def test_access_token_request_with_token_in_blocklist(self):
        Blocklist.add(self.access_token)

        payload = {"username": "test", "password": "test"}
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = self.client.post("/auth", json=payload, headers=headers)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json()["message"], "Token has been revoked")

    def test_fraud_prevention_request_with_empty_blocklist(self):
        payload = {"username": "test", "password": "test"}
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = self.client.post("/auth", json=payload, headers=headers)

        fresh_access_token = response.get_json()["access_token"]
        payload = {"transaction_id" : 2342357, "merchant_id" : self.account_id, "user_id" : 97051, "card_number" : "434505******9116", "transaction_date" : "2019-12-01T23:16:32.812632", "transaction_amount" : 373.56, "device_id" : 285475}
        headers = {"Authorization": f"Bearer {fresh_access_token}"}
        response = self.client.post("/risk/recommendation", json=payload, headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["transaction_id"], payload["transaction_id"])
        self.assertIn(response.get_json()["recommendation"], ["approve", "deny"])

    def test_fraud_prevention_request_with_token_in_blocklist(self):
        payload = {"username": "test", "password": "test"}
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = self.client.post("/auth", json=payload, headers=headers)

        fresh_access_token = response.get_json()["access_token"]
        Blocklist.add(fresh_access_token)

        payload = {"transaction_id" : 2342357, "merchant_id" : self.account_id, "user_id" : 97051, "card_number" : "434505******9116", "transaction_date" : "2019-12-01T23:16:32.812632", "transaction_amount" : 373.56, "device_id" : 285475}
        headers = {"Authorization": f"Bearer {fresh_access_token}"}
        response = self.client.post("/risk/recommendation", json=payload, headers=headers)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json()["message"], "Token has been revoked")
