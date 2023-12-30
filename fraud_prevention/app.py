import sys
sys.path.append('../../cloudwalk')

from flask import Flask, request, jsonify, make_response
from flask_limiter import Limiter
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from dotenv import load_dotenv
import datetime, os

from fraud_prevention.ml_fraud_risk import ml_fraud_risk
from fraud_prevention.rules_fraud_risk import rules_fraud_risk
from fraud_prevention.database.account import Account
from fraud_prevention.database.blocklist import Blocklist
from fraud_prevention.database.transaction import Transaction

load_dotenv()

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
app.config['JWT_ERROR_MESSAGE_KEY'] = 'message'

def get_remote_address():
    return request.remote_addr

limiter = Limiter(app=app, key_func=get_remote_address)
app.extensions['limiter'] = limiter

jwt = JWTManager(app=app)

@app.route("/private/token", methods=["POST"])
@limiter.limit("60/minute")
def create_token():
    allowed_ips = ['127.0.0.1'] # TODO: Replace with companies IP's only

    if request.remote_addr not in allowed_ips:
        return make_response(jsonify(message="Access not allowed"), 403)

    if not request.is_json:
        return make_response(jsonify(message="Missing JSON in request"), 400)

    account_id = request.json.get('account_id', None)

    if not account_id:
        return make_response(jsonify(message="Missing 'account_id' parameter"), 400)
    
    if not Account.exists(account_id):
        return make_response(jsonify(message="Invalid account"), 401)

    access_token = create_access_token(identity=account_id, fresh=False, expires_delta=False)
    return make_response(jsonify(access_token=access_token), 201)

@app.route("/login", methods=["POST"])
@jwt_required(fresh=False)
@limiter.limit("10/hour;3/minute")
def login():
    account_id = get_jwt_identity()

    if not Account.exists(account_id):
        return make_response(jsonify(message="Invalid account"), 401)

    if not request.is_json:
        return make_response(jsonify(message="Missing JSON in request"), 400)

    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if username != "test" or password != "test": # TODO: Replace with a valid authentication method
        return make_response(jsonify(message="Invalid username or password"), 401)

    identity = f"{account_id}|{username}"
    expires_in = int(os.getenv("FRESH_TOKEN_EXPIRES_IN_SECONDS", 300))
    access_token = create_access_token(identity=identity, fresh=True, expires_delta=datetime.timedelta(seconds=expires_in))

    return make_response(jsonify(access_token=access_token), 201)

@app.route("/fraud_prevention", methods=["POST"])
@jwt_required(fresh=True)
@limiter.limit("2/minute")
def fraud_prevention():
    if not request.is_json:
        return make_response(jsonify(message="Missing JSON in request"), 400)
    
    data = request.get_json()

    for field in ["transaction_id", "merchant_id", "user_id", "card_number", "transaction_amount", "device_id", "transaction_date"]:
        if field not in data or data[field] is None:
            return make_response(jsonify(message="Missing '%s' field" % field), 400)
        
    try:
        data["transaction_date"] = datetime.datetime.strptime(data["transaction_date"], "%Y-%m-%dT%H:%M:%S.%f")
    except:
        return make_response(jsonify(message="Invalid 'transaction_date' field. Expected format: YYYY-MM-DDTHH:MM:SS.MS"), 400)
    
    account_id = get_jwt_identity().split("|")[0]

    if int(account_id) != int(data["merchant_id"]) or not Account.exists(account_id):
        return make_response(jsonify(message="Invalid merchant"), 401)
    
    rules_recommendation = rules_fraud_risk(data)
    ml_recommendation = ml_fraud_risk(data)
    recommendation = "approve" if rules_recommendation and ml_recommendation else "deny"

    response = {
        "transaction_id": data["transaction_id"],
        "recommendation": recommendation
    }

    return make_response(jsonify(response), 200)

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return Blocklist.exists(jti)

Account.app = app
Account.load()
Blocklist.app = app
Blocklist.load()
Transaction.app = app
Transaction.load()
