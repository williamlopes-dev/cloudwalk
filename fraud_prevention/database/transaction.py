import csv, datetime

class Transaction:
    app = None
    database = {}

    @staticmethod
    def load():
        Transaction.database = {}
        with open('../files/transactional-sample.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['transaction_date'] = datetime.datetime.strptime(row['transaction_date'], "%Y-%m-%dT%H:%M:%S.%f")
                Transaction.database[int(row['transaction_id'])] = row

    @staticmethod
    def exists(transaction_id):
        try:
            return int(transaction_id) in Transaction.database
        except Exception as e:
            Transaction.app.logger.info(f"An error occurred: {e}")
            return False

    @staticmethod
    def find_by_transaction_id(transaction_id):
        try:
            return Transaction.database[transaction_id]
        except Exception as e:
            Transaction.app.logger.info(f"An error occurred: {e}")
            return None

    @staticmethod
    def find_by_user_id(user_id):
        try:
            filtered_transactions = []
            for transaction in Transaction.database.values():
                if int(transaction["user_id"]) == int(user_id):
                    filtered_transactions.append(transaction)
            return filtered_transactions
        except Exception as e:
            Transaction.app.logger.info(f"An error occurred: {e}")
            return None

    @staticmethod
    def add(transaction):
        try:
            Transaction.database[transaction["transaction_id"]] = transaction
            return True
        except Exception as e:
            Transaction.app.logger.info(f"An error occurred: {e}")
            return False
