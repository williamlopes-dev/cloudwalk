import sys
sys.path.append("../../../cloudwalk")

import datetime, os

from fraud_prevention.database.transaction import Transaction

def rules_fraud_risk(data):
    return many_transactions_in_a_row(data) or high_amount_in_risk_hours(data) or has_chargeback(data)

def many_transactions_in_a_row(data):
    max_transactions_allowed = int(os.getenv("TRANSACTIONS_IN_A_ROW_MAX_ALLOWED", 3))

    transactions = Transaction.find_by_user_id(data["user_id"])

    if not transactions or len(transactions) <= max_transactions_allowed:
        return False

    x_seconds = int(os.getenv("TRANSACTIONS_IN_A_ROW_WINDOW_IN_SECONDS", 600))
    transactions_in_last_x_seconds = []
    for transaction in transactions:
        if transaction["transaction_date"] >= data["transaction_date"] - datetime.timedelta(seconds=x_seconds):
            transactions_in_last_x_seconds.append(transaction)

    return len(transactions_in_last_x_seconds) > max_transactions_allowed

def high_amount_in_risk_hours(data):
    transaction_hour = data["transaction_date"].hour
    transaction_amount = float(data["transaction_amount"])

    start_hour = int(os.getenv("HIGH_AMOUNT_IN_RISK_HOURS_START", 21))
    end_hour = int(os.getenv("HIGH_AMOUNT_IN_RISK_HOURS_END", 8))
    max_amount = float(os.getenv("HIGH_AMOUNT_IN_RISK_MAX_AMOUNT", 500))

    return (transaction_hour >= start_hour or transaction_hour <= end_hour) and transaction_amount > max_amount

def has_chargeback(data):
    transactions = Transaction.find_by_user_id(data["user_id"])
    if not transactions:
        return False
    
    for transaction in transactions:
        if transaction["has_cbk"]:
            return True

    return False
