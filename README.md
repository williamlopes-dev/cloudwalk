# Answers
## 2. Tasks
### 2.1. Understand the Industry

1. Explain the money flow, the information flow, and the role of the main players in the payment industry.
    > The money flow could be explained starting from buyer account, passing by (sub-)acquirer and finishing in seller account.
    
    > The information flow could be explained with credit card data, like card holder name, card number, card verification code, expiratoin date, etc, encrypted and transitioned between bank accounts of the previows step.

    > The role of the main players is to guarantee the safety of occurred transactions between real people and companies, transferring money between bank accounts, and blocking any type of fraud/risk attempts.

2. Explain the difference between acquirer, sub-acquirer, and payment gateway, and how the flow explained in the previous question changes for these players.
    > All of that could be explained through a step by step flow, like: 1) payment gateway: receives buyer and order informations and sends to 2) sub-acquirer: receives data and do some validations, like risk/fraud prevention, and sends to 3) acquirer: receives the transaction request and make validations, like account balance, account status (blocked?), risk prevention, and approve it or denies the transaction. If approved, the money will be out from buyer bank account and will be in to seller bank account, the money will pass through acquirer/sub-acquirer bank accounts too.

3. Explain what chargebacks are, how they differ from a cancellation and what is their connection with fraud in the acquiring world.
    > Chargebacks happens when customers do not receive their products and the seller company guarantee that the products were sent. So they are in conflict and the chargeback exists to solve this problem, where each side will send documents to prove their point of view.

    > The difference between chargeback and cancellation is the "conflict" situation. Because in a charge cancellation, both sides agree with terms, in a chargeback is the opposite, they disagree from each other.

### 2.2. Solve the problem
A client sends you an email asking for a chargeback status. You check the system and see that we have received his defense documents and sent them to the issuer, but the issuer has not accepted our defense. They claim that the cardholder continued to affirm that she did not receive the product, and our documents were not sufficient to prove otherwise.

You respond to our client informing that the issuer denied the defense, and the next day he emails you back, extremely angry and disappointed, claiming the product was delivered and that this chargeback is not right.

Considering that the chargeback reason is “Product/Service not provided”, what would you do in this situation?
> I will inform the client about current chargeback status, being clear about issuer responsability in this process, saying that I understand that the current situation can be frustrating and I will suggest him to collect other proves to send us extra information, like security cameras, individual testimonials, delivery receipts, screenshots, chatting between both, etc.

> As an extra point, I will send a documentation in order to guarantee that the situation never happens again, doing some adjusts in his delivery process, like photos and videos boxing expensive produtcs, tracking logs with receiver signature (delivery receipt) on each delivery.

## 3. Get your hands dirty
Attached is a spreadsheet with hypothetical transactional data. Imagine that you are trying to understand if there is any kind of suspicious behavior.
1. Analyze the data provided and present your conclusions.
    > With just this dataset is hard to solve the fraud transactions problem, because we have only "transactions data", but it is a beginning and some aspects we can bring up. Like chargebacks by hour, "what hours have more risk?", or by chargebacks by MII, "what issuers are frequently with chargebacks issues?", or calculate the average amount by merchant and check the new transaction if amount is between min and max amount accepted, remembering to check standard deviation, because some merchant could sell products/services along with big price differences. However, we have some simple patterns to analyse too, like frequency of transactions using the same credit card, or credit card used in different devices, users, merchants in a small window time.

    > On the other hand, we can check if merchant was register correctly and if the information are really true, also check how many customers have accepted the transaction by merchant and kick out all merchants who has a small percentage of accepted transactions.

2. In addition to the spreadsheet data, what other data would you look at to try to find patterns of possible fraud?
    > Location based on IP, customer score (like Serasa), lifetime score (how much approves/denies/chargebacks?, number of credit cards used by year, nominal cards or borrowed cards?), buyer behavior (week days, average amount, merchants, monthly amount).

3. Considering your conclusions, what could you do to prevent fraud and/or chargebacks?
    > TLDR; create a set of params that will score the merchant and the customer based on historical behavior and current profile. At the same time only allow bigger limits after some initial validation, create a rule to transfer only transaction money to merchant bank account after X days.

4. How would you monitor identified patterns?
    > Creating a data routine to score after each transaction and chargeback (at start and finish).

    > Collecting more detailed info about transactions, merchants and customers.

    > Collecting data from thid-part platforms to do cross validation with my own data.

    > Implementing in my "seller" device a structure to validation merchant and customer profiles.

---
# Project
## Data analysis
### Review
I think that is not a really good dataset to analyse, could be more balanced among true/false chargebacks. If we have more data by customer/merchant, we also will be able to do other types of analysis. But, I have extracted some new informations using the own data, like Major Industry Identifier (MII), transaction hour and transaction week day, these new informations growed the precision to almost 10%. Finally, using RandomForestClassifier, I achived 92% of precision based on f1-score weighted average.

### Step by step
1. **Check inconsistences**: Not found.

   ![image](https://github.com/williamlopes-dev/cloudwalk/assets/7537086/bf7f2663-bbb1-492c-ba5d-671b449b9f1f)

1. **Check data balancing**: Too few chargebacks compared to ok transactions, at least 75% of the customers have a signel transaction and should be more balanced.

   ![image](https://github.com/williamlopes-dev/cloudwalk/assets/7537086/9ba812ad-6456-4128-a4fe-005acc92d18e)

1. **Fill missing values**: Add 999999 to device_id when null.

   ![image](https://github.com/williamlopes-dev/cloudwalk/assets/7537086/0399b574-1726-4f22-a6e5-5ea0d97c1e2c)

1. **Treat data**: Convert datetime, remove null values (not necessary here), convert credit card number to integer.

   ![image](https://github.com/williamlopes-dev/cloudwalk/assets/7537086/bdf5e1db-38a1-4535-a4a8-e7135519c607)

1. **Analyse converging data**: Analyse transaction by hour, week day and MII was a great converging way.

   ![image](https://github.com/williamlopes-dev/cloudwalk/assets/7537086/6a0090b2-7c3a-4bd2-ae36-cf2aa3bfded7)
   ![image](https://github.com/williamlopes-dev/cloudwalk/assets/7537086/78ce391a-7b12-4987-9979-7df5fd936540)
   ![image](https://github.com/williamlopes-dev/cloudwalk/assets/7537086/85d9ed1d-803d-4752-b366-f10d9e66e70c)
   ![image](https://github.com/williamlopes-dev/cloudwalk/assets/7537086/ac117fa5-1bff-4657-a062-f180a438e1e3)
   ![image](https://github.com/williamlopes-dev/cloudwalk/assets/7537086/fd8dfb0e-f876-4533-b957-bcf5ca37afd5)
   ![image](https://github.com/williamlopes-dev/cloudwalk/assets/7537086/2ccb7d9f-0b97-4f46-b482-0f440996e8d6)

1. **Prepare train and test data**: Select columns to be utilized, split data, prepare classifier and optimize params with rebalancing options.

   ![image](https://github.com/williamlopes-dev/cloudwalk/assets/7537086/69415aa4-9871-4603-959c-2c4433f9d769)

1. **Validate results**: The model was good to validate when has no chargeback, 96% using f1-score metric. But, when validating a true chargeback, the result was only 68%, will be needed more data.

   ![image](https://github.com/williamlopes-dev/cloudwalk/assets/7537086/1fac0e4f-e060-4308-a769-53b2b80159ac)

## Software
This software was projected to guarantee a good level of security, so it was implemented with:
- Forced ssl connection.
- JWT authentication.
- Token blocklist.
- Token expiration.
- Refresh token.
- Private endpoints by allowed IPs.
- Account validation to prevent unauthorized access between different accounts.

### Token system
We generate a access token for each account, these tokens won't expire by themselves. We can block any token, any time too. The client will use the account access token and username/password to generate your own fresh access token. The fresh access token generated will used on fraud recommendation endpoint and any other part of the software desired. With the token system implemented, we can guarantee:
- Block any access at any time by token.
- If the client lost your username/password, the hacker can't access without the account access token.
- If the client lost your token, the hacker can't access without the username/password.
- Fresh tokens will invalidate yourseves after a specific period without renew the token.

### Configuration
Put all of your configuration in the file `fraud_prevention/.env`.

* `JWT_SECRET_KEY`:
    * **Description**: Specifies the secret key used to generate JWT tokens.
    * **Default value**: f60bd1ecb1b9a8f0784c49ad0cce9700c74980f2898fd37673fc31223d7419dd
* `PRIVATE_IPS`: 
    * **Description**: Specifies the allowed IPs to access private endpoints.
    * **Default value**: `127.0.0.1`
* `FRESH_TOKEN_EXPIRES_IN_SECONDS`:
    * **Description**: Specifies the time in seconds that a fresh access token will be valid.
    * **Default value**: 600 (10 minutes)
* `TRANSACTIONS_IN_A_ROW_MAX_ALLOWED`: 
    * **Description**: Specifies the maximum number of consecutive transactions allowed within a certain time window.
    * **Default value**: 5
* `TRANSACTIONS_IN_A_ROW_WINDOW_IN_SECONDS`: 
    * **Description**: Specifies the time window in seconds within which consecutive transactions are counted.
    * **Default value**: 1800 (30 minutes)
* `HIGH_AMOUNT_IN_RISK_HOURS_START`: 
    * **Description**: Specifies the start hour of the high-risk period for transactions with high amounts.
    * **Default value**: 22 (10 PM)
* `HIGH_AMOUNT_IN_RISK_HOURS_END`: 
    * **Description**: Specifies the end hour of the high-risk period for transactions with high amounts.
    * **Default value**: 6 (6 AM)
* `HIGH_AMOUNT_IN_RISK_HOURS_MAX_AMOUNT`: 
    * **Description**: Specifies the maximum amount allowed for transactions during the high-risk period.
    * **Default value**: 1000

### Versions
- Python 3.8.9
- Pip 23.3.2
- Install dependencies:
    ```
    cd cloudwalk
    pip install -r requirements.txt
    ```

### Run tests
```shell
cd cloudwalk/tests
python3 -m unittest
```

### Run server
```shell
cd cloudwalk/fraud_prevention
python3 server.py
```
> **Observations**: Only username=`test` and password=`test` are allowed. The `merchant_id` is considered `account_id`, so only the identifiers of `merchant_id` column in `files/transactional-sample.csv` will be treated like a valid account.

### API documentation
* **POST** `/private/token`
    * **Description**:
        * Generates an access token for the API.
        * This token does not expire and is used to generate an exclusive fresh access token for the requested account.
        * **Important**: This endpoint is only available for configured CloudWalk IPs and can be changed using `PRIVATE_IPS` env var.
    * **Body** `application/json`:
        * **account_id** `integer`: Account ID.
    * **Response**:
        * **token** `string`: Access token.
    * **Example** with `curl`:
        ```shell
        curl -k -X POST \
        https://localhost:5000/private/token \
        -H 'Content-Type: application/json' \
        -d '{
            "account_id": <account_id>
        }'
        ```
* **DELETE** `/private/token/block`
    * **Description**:
        * Adds an access token to blocklist.
        * Any access token type is allowed, fresh or not.
        * **Important**: This endpoint is only available for configured CloudWalk IPs and can be changed using `PRIVATE_IPS` env var.
    * **Body** `application/json`:
        * **token** `string`: Access token.
    * **Example** with `curl`:
        ```shell
        curl -k -X DELETE \
        https://localhost:5000/private/token/block \
        -H 'Content-Type: application/json' \
        -d '{
            "token": "<token>"
        }'
        ```
* **POST** `/auth`
    * **Description**:
        * Generates an fresh access token for the API.
        * This token expire in 10 minutes by default and can be changed using `FRESH_TOKEN_EXPIRES_IN_SECONDS` env var, 60 seconds is the minimum value accepted.
        * The fresh access token can be refreshed using accessing `/auth/refresh` endpoint.
        * **Important**: This token is used to perform all authenticated requests. If exposed, this fresh access token can be added to blocklist internally or when expired.
    * **Header**:
        * **Authorization** `string`: Access token. **Format**: `Bearer <token>`
    * **Body** `application/json`:
        * **username** `string`: Username.
        * **password** `string`: Password.
    * **Response**:
        * **token** `string`: Fresh access token.
    * **Example** with `curl`:
        ```shell
        curl -k -X POST \
        https://localhost:5000/auth \
        -H 'Content-Type: application/json' \
        -H 'Authorization: Bearer <token>' \
        -d '{
            "username": "<username>",
            "password": "<password>"
        }'
        ```
* **GET** `/auth/refresh`
    * **Description**:
        * Renews an expiring but still active fresh access token.
        * This token expire in 10 minutes by default and can be changed using `FRESH_TOKEN_EXPIRES_IN_SECONDS` env var, 60 seconds is the minimum value accepted.
        * This token is used to perform any authenticated requested.
    * **Header**:
        * **Authorization** `string`: Fresh access token. **Format**: `Bearer <token>`
    * **Response**:
        * **token** `string`: New fresh access token.
    * **Example** with `curl`:
        ```shell
        curl -k -X GET \
        https://localhost:5000/auth/refresh \
        -H 'Content-Type: application/json' \
        -H 'Content-Type: application/json' \
        -H 'Authorization: Bearer <token>'
        ```
* **DELETE** `/auth/expire`
    * **Description**:
        * Expires an active fresh access token.
    * **Header**:
        * **Authorization** `string`: Fresh access token. **Format**: `Bearer <token>`
    * **Example** with `curl`:
        ```shell
        curl -k -X DELETE \
        https://localhost:5000/auth/expire \
        -H 'Content-Type: application/json' \
        -H 'Content-Type: application/json' \
        -H 'Authorization: Bearer <token>'
        ```
* **POST** `/risk/recommendation`
    * **Description**:
        * Returns a recommendation for a transaction.
    * **Header**:
        * **Authorization** `string`: Fresh access token. **Format**: `Bearer <token>`
    * **Body** `application/json`:
        * **transaction_id** `integer`: Transaction ID.
        * **merchant_id** `integer`: Merchant ID.
        * **user_id** `integer`: User ID.
        * **card_number** `string`: Card number. **Format**: `000000******0000`
        * **transaction_amount** `float`: Transaction amount.
        * **device_id** `integer`: Device ID.
        * **transaction_date** `datetime`: Transaction date. **Format**: `YYYY-MM-DDTHH:MM:SS.000000`
    * **Response**:
        * **transaction_id** `integer`: Transaction ID.
        * **recommendation** `string`: `approve` or `deny`.
    * **Example** with `curl`:
        ```shell
        curl -k -X POST \
        https://localhost:5000/risk/recommendation \
        -H 'Content-Type: application/json' \
        -H 'Authorization: Bearer <token>' \
        -d '{
            "transaction_id": <transaction_id>,
            "merchant_id": <merchant_id>,
            "user_id": <user_id>,
            "card_number": "<card_number>",
            "transaction_amount": <transaction_amount>,
            "device_id": <device_id>,
            "transaction_date": "<transaction_date>"
        }'
        ```
