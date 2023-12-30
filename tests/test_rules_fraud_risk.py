import sys
sys.path.append('../../cloudwalk')

from tests.base import Base

import datetime

from fraud_prevention.database.transaction import Transaction

from fraud_prevention.rules_fraud_risk import many_transactions_in_a_row, high_amount_in_risk_hours, has_chargeback

class RulesFraudRiskTests(Base):
    def setUp(self):
        super().setUp()
        Transaction.load()

    def test_rules_fraud_risk_6_transactions_in_a_row(self):
        data = {"transaction_id" : 1, "merchant_id" : 29744, "user_id" : 999999, "card_number" : "434505******9116", "transaction_date" : "2019-12-01T23:16:32.812632", "transaction_amount" : 373.56, "device_id" : 285475}
        data["transaction_date"] = datetime.datetime.strptime(data["transaction_date"], "%Y-%m-%dT%H:%M:%S.%f")

        for i in range(6):
            data = data.copy()
            data["transaction_id"] += i
            data["transaction_date"] += datetime.timedelta(minutes=1)
            data["has_cbk"] = False
            Transaction.add(data)

        self.assertTrue(many_transactions_in_a_row(data))

    def test_rules_fraud_risk_5_transactions_in_a_row(self):
        data = {"transaction_id" : 1, "merchant_id" : 29744, "user_id" : 999999, "card_number" : "434505******9116", "transaction_date" : "2019-12-01T23:16:32.812632", "transaction_amount" : 373.56, "device_id" : 285475}
        data["transaction_date"] = datetime.datetime.strptime(data["transaction_date"], "%Y-%m-%dT%H:%M:%S.%f")

        for i in range(5):
            data = data.copy()
            data["transaction_id"] += i
            data["transaction_date"] += datetime.timedelta(minutes=1)
            data["has_cbk"] = False
            Transaction.add(data)

        self.assertFalse(many_transactions_in_a_row(data))

    def test_rules_fraud_risk_in_risk_window_high_amount_in_risk_hours(self):
        data = {"transaction_id" : 1, "merchant_id" : 29744, "user_id" : 999999, "card_number" : "434505******9116", "transaction_date" : "2019-12-01T23:16:32.812632", "transaction_amount" : 1373.56, "device_id" : 285475}
        data["transaction_date"] = datetime.datetime.strptime(data["transaction_date"], "%Y-%m-%dT%H:%M:%S.%f")

        data["transaction_date"] = data["transaction_date"].replace(hour=23)

        self.assertTrue(high_amount_in_risk_hours(data))

    def test_rules_fraud_risk_in_risk_window_high_amount_in_risk_hours_but_lower_amount(self):
        data = {"transaction_id" : 1, "merchant_id" : 29744, "user_id" : 999999, "card_number" : "434505******9116", "transaction_date" : "2019-12-01T23:16:32.812632", "transaction_amount" : 373.56, "device_id" : 285475}
        data["transaction_date"] = datetime.datetime.strptime(data["transaction_date"], "%Y-%m-%dT%H:%M:%S.%f")

        data["transaction_date"] = data["transaction_date"].replace(hour=23)

        self.assertFalse(high_amount_in_risk_hours(data))

    def test_rules_fraud_risk_out_of_risk_window_high_amount_in_risk_hours(self):
        data = {"transaction_id" : 1, "merchant_id" : 29744, "user_id" : 999999, "card_number" : "434505******9116", "transaction_date" : "2019-12-01T23:16:32.812632", "transaction_amount" : 1373.56, "device_id" : 285475}
        data["transaction_date"] = datetime.datetime.strptime(data["transaction_date"], "%Y-%m-%dT%H:%M:%S.%f")

        data["transaction_date"] = data["transaction_date"].replace(hour=9)

        self.assertFalse(high_amount_in_risk_hours(data))

    def test_rules_fraud_risk_true_has_chargeback(self):
        data = {"transaction_id" : 1, "merchant_id" : 29744, "user_id" : 999999, "card_number" : "434505******9116", "transaction_date" : "2019-12-01T23:16:32.812632", "transaction_amount" : 1373.56, "device_id" : 285475}
        data["transaction_date"] = datetime.datetime.strptime(data["transaction_date"], "%Y-%m-%dT%H:%M:%S.%f")
        data["has_cbk"] = True
        Transaction.add(data)

        data = data.copy()
        data["transaction_id"] = 2
        data["transaction_date"] += datetime.timedelta(minutes=1)

        self.assertTrue(has_chargeback(data))

    def test_rules_fraud_risk_false_has_chargeback(self):
        data = {"transaction_id" : 1, "merchant_id" : 29744, "user_id" : 999999, "card_number" : "434505******9116", "transaction_date" : "2019-12-01T23:16:32.812632", "transaction_amount" : 1373.56, "device_id" : 285475}
        data["transaction_date"] = datetime.datetime.strptime(data["transaction_date"], "%Y-%m-%dT%H:%M:%S.%f")
        data["has_cbk"] = False
        Transaction.add(data)

        data = data.copy()
        data["transaction_id"] = 2
        data["transaction_date"] += datetime.timedelta(minutes=1)

        self.assertFalse(has_chargeback(data))