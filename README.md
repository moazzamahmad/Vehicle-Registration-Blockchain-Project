# Vehicle-Registration-Blockchain-Project

A simple blockchain implementation in Python for recording **vehicle registration and ownership transfer transactions**. This repository includes:

* `blockchain.py` — core blockchain and block implementation
* `app.py` — Flask API to interact with the blockchain
* `requirements.txt` — Python dependencies
* `README.md` — project overview, setup, and API documentation
* `.gitignore` — common ignores
* `tests/test_blockchain.py` — basic unit tests using pytest

---

## File: README.md

````markdown
# Vehicle Registration Blockchain

Simple Python blockchain to record vehicle registration, ownership transfers, and related transactions.

## Features
- Add vehicle registration transactions
- Mine blocks (proof-of-work) to append transactions to the ledger
- View full chain
- Validate chain integrity
- Query vehicle history by registration number

## Tech stack
- Python 3.10+
- Flask (lightweight API)
- hashlib for SHA-256

## Setup
1. Create a virtual environment:
```bash
python -m venv env
source env/bin/activate  # macOS / Linux
env\Scripts\activate     # Windows
````

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the API server:

```bash
python app.py
```

The server runs by default on `http://127.0.0.1:5000`.

## API Endpoints

* `POST /add_transaction` — add a pending vehicle registration transaction

  * Body (json):

    ```json
    {
      "vehicle_id": "MH12AB1234",
      "previous_owner": "Bob",
      "new_owner": "Alice",
      "price": 500000,
      "transaction_type": "transfer"
    }
    ```
* `GET /mine_block` — Mine a new block containing pending transactions
* `GET /get_chain` — Return the whole blockchain
* `GET /is_valid` — Check if blockchain is valid
* `GET /vehicle_history/<vehicle_id>` — Returns all transactions for a vehicle

## Example usage (curl)

1. Add a transaction

```bash
curl -X POST http://127.0.0.1:5000/add_transaction -H "Content-Type: application/json" -d '{"vehicle_id":"MH12AB1234","previous_owner":"Bob","new_owner":"Alice","price":500000,"transaction_type":"transfer"}'
```

2. Mine a block

```bash
curl http://127.0.0.1:5000/mine_block
```

3. Get chain

```bash
curl http://127.0.0.1:5000/get_chain
```

## Tests

Run tests with pytest:

```bash
pytest -q
```

## Notes

This is a teaching/simple prototype. Do not use this for production legal records.

```
```

---

## File: requirements.txt

```
Flask>=2.0
pytest
requests
```

---

## File: .gitignore

```
__pycache__/
env/
.env
.DS_Store
*.pyc
```

---

