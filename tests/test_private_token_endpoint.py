import sys
sys.path.append("../../cloudwalk")

from tests.base import Base

class TestPrivateTokenEndpoint(Base):
    def setUp(self):
        super().setUp()
        self.account_id = 29744

    def test_private_token_request_with_valid_params(self):
        payload = {"account_id": self.account_id}
        response = self.client.post("/private/token", json=payload)

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.get_json()["access_token"])

    def test_private_token_request_with_invalid_params(self):
        payload = {"account_id": 999999}
        response = self.client.post("/private/token", json=payload)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json()["message"], "Invalid account")

    def test_private_token_request_without_params(self):
        payload = {}
        response = self.client.post("/private/token", json=payload)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["message"], "Missing 'account_id' field")

    def test_private_token_request_without_payload(self):
        payload = None
        response = self.client.post("/private/token", json=payload)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["message"], "Missing JSON in request")

    def test_private_token_block_request_with_access_token(self):
        payload = {"account_id": self.account_id}
        response = self.client.post("/private/token", json=payload)

        self.assertEqual(response.status_code, 201)
        access_token = response.get_json()["access_token"]

        payload = {"token": access_token}
        response = self.client.delete("/private/token/block", json=payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["message"], "Token added to blocklist")

        response = self.client.post("/auth", headers={"Authorization": f"Bearer {access_token}"})

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json()["message"], "Token has been revoked")

    def test_private_token_block_request_with_fresh_access_token(self):
        payload = {"account_id": self.account_id}
        response = self.client.post("/private/token", json=payload)

        self.assertEqual(response.status_code, 201)
        access_token = response.get_json()["access_token"]

        payload = {"username": "test", "password": "test"}
        headers = {"Authorization": f"Bearer {access_token}"}
        response = self.client.post("/auth", json=payload, headers=headers)

        self.assertEqual(response.status_code, 201)
        
        fresh_access_token = response.get_json()["access_token"]
        payload = {"token": fresh_access_token}
        self.client.delete("/private/token/block", json=payload)

        response = self.client.get("/auth/refresh", headers={"Authorization": f"Bearer {fresh_access_token}"})

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json()["message"], "Token has been revoked")

    def test_private_token_block_request_without_token(self):
        payload = {}
        response = self.client.delete("/private/token/block", json=payload)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["message"], "Missing 'token' field")