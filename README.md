# CoinTracker_Assignment
# CoinTracker Wallet Tracking Service

## Overview

This project is a lightweight CoinTracker-style prototype that allows users to track Bitcoin wallet addresses and retrieve real-time on-chain wallet information. The service exposes a RESTful API that supports adding and listing tracked wallets, as well as fetching current balances and aggregate transaction counts for each address.

The implementation focuses on delivering a fully working v0.1 system with clean architecture, clear separation of concerns, and reproducible local setup, while intentionally avoiding unnecessary complexity such as background workers or heavy data modeling.

---

## Features

- Add and track Bitcoin wallet addresses
- Prevent duplicate or invalid wallet tracking
- Retrieve real-time wallet balance (BTC)
- Retrieve aggregate transaction count per wallet
- Lightweight persistence using SQLite
- External blockchain data integration via BlockCypher API

---

## Tech Stack

- **Language:** Python 3.10+
- **Web Framework:** Flask
- **Database:** SQLite
- **HTTP Client:** Requests
- **Blockchain Provider:** BlockCypher API
- **Development Environment:** Virtualenv

---

## Project Structure
cointracker-wallet-service/
├── app/
│ ├── api/
│ │ └── routes.py # API route definitions
│ ├── services/
│ │ ├── wallet_service.py # Business logic
│ │ └── blockchain_service.py# External blockchain integration
│ ├── db/
│ │ └── database.py # SQLite persistence layer
│ ├── utils/
│ │ └── btc_validator.py # Bitcoin address validation
│ └── main.py # Flask app factory
├── run.py # Application entry point
├── requirements.txt
├── .gitignore
└── README.md



---

## API Endpoints

### Add Wallet

**POST** `/api/wallets`

```json
{
  "address": "3E8ociqZa9mZUSwGdSmAEMAoAxBK3FNDcd"
}

{
  "status": "tracking",
  "address": "3E8ociqZa9mZUSwGdSmAEMAoAxBK3FNDcd"
}

GET /api/wallets

Response :
{
  "wallets": [
    "3E8ociqZa9mZUSwGdSmAEMAoAxBK3FNDcd"
  ],
  "count": 1
}

GET /api/wallets/<address>
{
  "address": "3E8ociqZa9mZUSwGdSmAEMAoAxBK3FNDcd",
  "balance_btc": 0.00026169,
  "total_transactions": 2017
}

Local Setup :

git clone https://github.com/<your-username>/cointracker-wallet-service.git
cd cointracker-wallet-service

# Important Terminal Command

# Create and activate virtual Environment :
python -m venv venv

# Actiavte the virtual Environments
venv\Scripts\activate

# Installing Dependencies 
pip install -r requirements.txt

# Run the application 
python run.py

Testing 


Invoke-RestMethod `
  -Uri "http://127.0.0.1:5000/api/wallets" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"address":"3E8ociqZa9mZUSwGdSmAEMAoAxBK3FNDcd"}'


Conclusion :

This project demonstrates a clean, maintainable approach to building a wallet tracking service with clear separation of concerns and real-world blockchain integration. The architecture is intentionally kept simple while remaining extensible for future production-grade enhancements.


Assumptions Made During Development

1.The application is designed as a single-user, local prototype, so wallet ownership, authentication, and access control are intentionally out of scope.
2.Only Bitcoin mainnet addresses are supported. Testnet and other networks are excluded to keep validation and blockchain queries straightforward.
3.Wallet addresses are validated using format-based checks only (legacy and SegWit patterns). Deeper validation such as checksum verification or on-chain existence is delegated to the blockchain data provider.
4.Wallet data (balance and transaction count) is fetched on demand rather than continuously synchronized. This avoids unnecessary background processing and ensures up-to-date results when queried.
5.Only confirmed balances are returned, as provided by the external API, and unconfirmed or mempool transactions are not included.
6.Transaction history is treated as an aggregate metric (total transaction count) rather than storing individual transactions, which keeps the data model simple and avoids large storage overhead for high-activity wallets.
7.SQLite is used for persistence under the assumption that this is a lightweight demo environment. The schema is intentionally minimal and optimized for fast local setup rather than horizontal scalability.
8.The system assumes reasonable API availability from the blockchain provider and does not implement retries or rate-limit handling beyond basic timeout protection.
9.The application is expected to be run in a trusted local or development environment, so advanced security measures such as API authentication, encryption at rest, and request throttling are not implemented.
