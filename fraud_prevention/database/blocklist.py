import os
from flask_jwt_extended import decode_token
from jwt import ExpiredSignatureError

class Blocklist:
    app = None
    database = set()
    filename = '../files/blocklist-sample.txt'
    last_modified = 0.0

    @staticmethod
    def load():
        Blocklist.database = set()
        with open(Blocklist.filename, 'r') as file:
            for row in file:
                access_token = row.strip()
                try:
                    with Blocklist.app.app_context():
                        jwt_payload = decode_token(access_token)
                    Blocklist.database.add(jwt_payload['jti'])
                except ExpiredSignatureError as e:
                    pass # ignore expired tokens
        Blocklist.last_modified = os.path.getmtime(Blocklist.filename)

    @staticmethod
    def exists(access_token):
        Blocklist.check_file_and_load()
        try:
            return access_token in Blocklist.database
        except Exception as e:
            Blocklist.app.logger.error(f"An error occurred: {e}")
            return False
    
    @staticmethod
    def check_file_and_load():
        current_modified = os.path.getmtime(Blocklist.filename)
        if current_modified != Blocklist.last_modified:
            Blocklist.load()
    
    @staticmethod
    def add(access_token):
        with open('../files/blocklist-sample.txt', 'a') as file:
            file.write("%s\n" % access_token)
    
    @staticmethod
    def clear():
        open(Blocklist.filename, 'w').close()
        Blocklist.load()