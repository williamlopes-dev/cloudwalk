import sys
sys.path.append("../../cloudwalk")

from flask import Flask, request, jsonify, make_response
from flask_limiter import Limiter
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from functools import wraps
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
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access"]
app.config["JWT_ERROR_MESSAGE_KEY"] = "message"

ALLOWED_IPS = os.getenv("PRIVATE_IPS", "127.0.0.1").split(",")

def get_remote_address():
    return request.remote_addr

limiter = Limiter(app=app, key_func=get_remote_address)
app.extensions["limiter"] = limiter

jwt = JWTManager(app=app)

def private(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.remote_addr not in ALLOWED_IPS:
            return make_response(jsonify(message="Access not allowed"), 403)

        return f(*args, **kwargs)
    return decorated_function

def account_required(source='header'):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if source == 'header':
                account_id = get_jwt_identity().split("|")[0]
            elif source == 'body':
                account_id = request.json.get("account_id")
            else:
                account_id = None

            if account_id is None or not Account.exists(account_id):
                return make_response(jsonify(message="Invalid account"), 401)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def json_required(fields=[]):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return make_response(jsonify(message="Missing JSON in request"), 400)
            
            data = request.get_json()
            if data is None:
                return make_response(jsonify(message="Invalid JSON"), 400)

            for field in fields:
                if field not in request.json or request.json[field] is None:
                    return make_response(jsonify(message="Missing '%s' field" % field), 400)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route("/private/token", methods=["POST"])
@private
@json_required(fields=["account_id"])
@account_required(source='body')
@limiter.limit("60/minute")
def private_token():
    account_id = request.json.get("account_id")
    username = "private"

    identity = f"{account_id}|{username}"

    access_token = create_access_token(identity=identity, fresh=False, expires_delta=False)
    return make_response(jsonify(access_token=access_token), 201)

@app.route("/private/token/block", methods=["DELETE"])
@private
@json_required(fields=["token"])
@limiter.limit("120/minute")
def private_token_block():
    token = request.json.get("token")

    Blocklist.add(token)
    return make_response(jsonify(message="Token added to blocklist"), 201)

@app.route("/auth", methods=["POST"])
@jwt_required(fresh=False)
@account_required(source='header')
@json_required(fields=["username", "password"])
@limiter.limit("10/hour;3/minute")
def auth():
    account_id = get_jwt_identity()

    username = request.json.get("username")
    password = request.json.get("password")

    if username != "test" or password != "test": # TODO: Replace with a valid authentication method
        return make_response(jsonify(message="Invalid username or password"), 401)
    
    access_token = generate_fresh_access_token(account_id, username)

    return make_response(jsonify(access_token=access_token), 201)

@app.route("/auth/refresh", methods=["GET"])
@jwt_required(fresh=True)
@account_required(source='header')
@limiter.limit("1/minute")
def auth_refresh():
    account_id = get_jwt_identity().split("|")[0]
    username = get_jwt_identity().split("|")[1]

    new_access_token = generate_fresh_access_token(account_id, username)
    
    current_access_token = request.headers.get("Authorization").split(" ")[1]
    Blocklist.add(current_access_token)

    return make_response(jsonify(access_token=new_access_token), 201)

@app.route("/auth/expire", methods=["DELETE"])
@jwt_required(fresh=True)
@account_required(source='header')
@limiter.limit("1/minute")
def auth_expire():
    access_token = request.headers.get("Authorization").split(" ")[1]
    Blocklist.add(access_token)
    return make_response(jsonify(message="Token was expired"), 201)

@app.route("/risk/recommendation", methods=["POST"])
@jwt_required(fresh=True)
@account_required(source='header')
@json_required(fields=["transaction_id", "merchant_id", "user_id", "card_number", "transaction_amount", "device_id", "transaction_date"])
@limiter.limit("2/minute")
def risk_recommendation():
    account_id = get_jwt_identity().split("|")[0]
    data = request.get_json()

    if int(account_id) != int(data["merchant_id"]):
        return make_response(jsonify(message="Invalid merchant"), 401)

    try:
        data["transaction_date"] = datetime.datetime.strptime(data["transaction_date"], "%Y-%m-%dT%H:%M:%S.%f")
    except:
        return make_response(jsonify(message="Invalid 'transaction_date' field. Expected format: YYYY-MM-DDTHH:MM:SS.MS"), 400)
    
    rules_recommendation = rules_fraud_risk(data)
    ml_recommendation = ml_fraud_risk(data)
    recommendation = "approve" if rules_recommendation and ml_recommendation else "deny"

    response = {
        "transaction_id": data["transaction_id"],
        "recommendation": recommendation
    }

    return make_response(jsonify(response), 200)

def generate_fresh_access_token(account_id, username):
    identity = f"{account_id}|{username}"
    expires_in = int(os.getenv("FRESH_TOKEN_EXPIRES_IN_SECONDS", 300))
    if expires_in < 60:
        expires_in = 60
    
    access_token = create_access_token(identity=identity, fresh=True, expires_delta=datetime.timedelta(seconds=expires_in))
    return access_token

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return Blocklist.exists(jti)

databases = [Account, Blocklist, Transaction]
for database in databases:
    database.app = app
    database.load()
