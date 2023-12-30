import sys
sys.path.append("../../../cloudwalk")

from joblib import load
import pandas as pd

def ml_fraud_risk(data):
    data = normalize(data)

    model = load("../files/model.joblib")
    ordered_columns = [
        "transaction_id",
        "merchant_id",
        "user_id",
        "transaction_amount",
        "device_id",
        "transaction_hour",
        "transaction_weekday",
        "mii"
    ]
    predictions = model.predict(pd.DataFrame([data], columns=ordered_columns))

    return predictions[0]

def normalize(data):
    expected_fields = [
        "transaction_id",
        "merchant_id",
        "user_id",
        "card_number",
        "transaction_amount",
        "device_id",
        "transaction_date"
    ]
    data = {key: data[key] for key in data.keys() if key in expected_fields}

    data["transaction_hour"] = data["transaction_date"].hour
    data["transaction_weekday"] = data["transaction_date"].weekday()

    data["mii"] = data["card_number"][0]

    if not data["device_id"]:
        data["device_id"] = 999999

    data.pop("transaction_date")
    data.pop("card_number")

    data = {key: float(value) if key == "transaction_amount" else int(value) for key, value in data.items()}

    return data