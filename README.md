# Answers
## 2. Tasks
### 2.1. Understand the Industry

1. Explain the money flow, the information flow, and the role of the main players in the payment industry.
    > The money flow could be explained starting from buyer account, passing by (sub-)acquirer and finishing in seller account.
    ---
    > The information flow could be explained with credit card data, like card holder name, card number, card verification code, expiratoin date, etc, encrypted and transitioned between bank accounts of the previows step.
    ---
    > The role of the main players is guarantee the transactions occurred with safety between real people and companies, transfering money between bank accounts, and blocking any type of fraud/risk attempts.

2. Explain the difference between acquirer, sub-acquirer, and payment gateway, and how the flow explained in the previous question changes for these players.
    > All of that could be explained with a step by step flow, like: 1) payment gateway: receives buyer and order informations and sends to 2) sub-acquirer: receives data and do some validations, like risk/fraud prevention, and sends to 3) acquirer: receives the transaction request and do some validations, like account balance, account status (blocked?), risk prevention, and approves or denies the transaction. If approved, the money will out from buyer bank account and get in to seller bank account, the money will pass by acquirer/sub-acquirer bank accounts too.

3. Explain what chargebacks are, how they differ from a cancellation and what is their connection with fraud in the acquiring world.
    > Chargesbacks are disputes when customers does not receives they products and the seller company said that were sent. So they are in conflict, and the chargeback exists to solve this problem, where each side will send documents to prove your point of view.
    ---
    > The difference between chargeback and cancellation is on "conflict" situation. Because in a charge cancellation, both side agree with terms, in a chargeback it's not true.

### 2.2. Solve the problem
A client sends you an email asking for a chargeback status. You check the system and see that we have received his defense documents and sent them to the issuer, but the issuer has not accepted our defense. They claim that the cardholder continued to affirm that she did not receive the product, and our documents were not sufficient to prove otherwise.

You respond to our client informing that the issuer denied the defense, and the next day he emails you back, extremely angry and disappointed, claiming the product was delivered and that this chargeback is not right.

Considering that the chargeback reason is “Product/Service not provided”, what would you do in this situation?
> I will inform the client about current chargeback status, be clear about issuer responsability in this process, to say that I understand this situation can be frustrating and I will suggest considering collecting other proves to send extra information, like security cameras, individual testimonials, delivery receipts, screenshots, chatting between both.
---
> As an extra point, I will send a documentation to guarantee that situation never happen again, doing some adjusts in his delivery process, like photos and videos boxing expensive produtcs, tracking logs with receiver signature (delivery receipt) on each delivery.

## 3. Get your hands dirty
Attached is a spreadsheet with hypothetical transactional data. Imagine that you are
trying to understand if there is any kind of suspicious behavior.
1. Analyze the data provided and present your conclusions.
    > With just this dataset is hard to solve the fraud transactions problem, because we have only "transactions data", but it is a beginning and some aspects we can bring up. Like chargebacks by hour, "what hours have more risk?", or by chargebacks by MII, "what issuers are frequently with chargebacks issues?", or calculate the average amount by merchant and check the new transaction if amount is between min and max amount accepted, but remeber to check standard deviation, because some merchant could sell products/services with big difference in their prices. However, we have some simple patterns to analyse too, like frequency of transactions with the same credit card, or credit card used in different devices, users, merchants in a small window time.
    ---
    > In the other hand, we can check if merchant was register correctly and if the information are really true, also check how much customers have accepted the transaction by merchant and kick out all merchants who has a small percent of accepted transactions.

2. In addition to the spreadsheet data, what other data would you look at to try to
find patterns of possible fraud?
    > Location based on IP, customer score (like Serasa), lifetime score (how much approves/denies/chargebacks?, number of used credit cards by year, nominal cards or borrowed cards?), buyer behavior (week days, average amount, merchants, monthly amount).

3. Considering your conclusions, what could you do to prevent fraud and/or
chargebacks?
    > TLDR; create a set of params that will score the merchant and the customer based on historical behavior and current profile. At the same time only allow bigger limits after some initial validation, create a rule to only transfer transaction money to merchant bank account after X days.

4. How would you monitor identified patterns?
    > Creating a data routine to score after each transaction and chargeback (at start and finish).
    ---
    > Collecting more detailed info about transactions, merchants and customers.
    ---
    > Collecting data from thid-part platforms to do cross validation with my own data.
    ---
    > Implementing in my "seller" device a structure to validation merchant and customer profiles.

---
# Project
## Data analysis
## Fraud prevent endpoint
### Run server
```shell
cd cloudwalk/fraud_prevention
python3 server.py
```
### Run tests
```shell
cd cloudwalk/tests
python3 -m unittest
```