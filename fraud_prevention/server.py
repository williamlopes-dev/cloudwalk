import sys
sys.path.append('../../cloudwalk')

from fraud_prevention.app import app

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True, ssl_context="adhoc")