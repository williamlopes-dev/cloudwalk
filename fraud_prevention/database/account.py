import csv

class Account:
    app = None
    database = set()

    @staticmethod
    def load():
        Account.database = set()
        with open('../files/transactional-sample.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Account.database.add(int(row['merchant_id']))


    @staticmethod
    def exists(account_id):
        try:
            return int(account_id) in Account.database
        except Exception as e:
            Account.app.logger.info(f"An error occurred: {e}")
            return False
