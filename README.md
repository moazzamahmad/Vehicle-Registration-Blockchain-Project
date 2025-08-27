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

## File: blockchain.py

```python
# blockchain.py
from __future__ import annotations
import hashlib
import json
from time import time
from typing import List, Dict, Any


class Block:
    def __init__(self, index: int, timestamp: float, transactions: List[Dict[str, Any]], previous_hash: str, nonce: int = 0):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        """Compute SHA-256 hash of the block's contents."""
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    difficulty = 3  # number of leading zeros required in the hash

    def __init__(self):
        self.chain: List[Block] = []
        self.pending_transactions: List[Dict[str, Any]] = []
        self.create_genesis_block()

    def create_genesis_block(self) -> None:
        genesis_block = Block(0, time(), [
            {
                'vehicle_id': 'GENESIS',
                'previous_owner': None,
                'new_owner': None,
                'price': 0,
                'transaction_type': 'genesis'
            }
        ], previous_hash='0')
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    def proof_of_work(self, block: Block) -> str:
        block.nonce = 0
        computed_hash = block.compute_hash()
        target = '0' * self.difficulty
        while not computed_hash.startswith(target):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_block(self, block: Block, proof: str) -> bool:
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block: Block, block_hash: str) -> bool:
        return (block_hash.startswith('0' * self.difficulty) and block_hash == block.compute_hash())

    def add_new_transaction(self, transaction: Dict[str, Any]) -> int:
        required_fields = ['vehicle_id', 'previous_owner', 'new_owner', 'price', 'transaction_type']
        for field in required_fields:
            if field not in transaction:
                raise ValueError(f"Missing field {field} in transaction")
        self.pending_transactions.append(transaction)
        return self.last_block.index + 1

    def mine(self) -> Block:
        if not self.pending_transactions:
            raise RuntimeError('No transactions to mine')
        new_block = Block(index=self.last_block.index + 1,
                          timestamp=time(),
                          transactions=self.pending_transactions.copy(),
                          previous_hash=self.last_block.hash)
        proof = self.proof_of_work(new_block)
        added = self.add_block(new_block, proof)
        if not added:
            raise RuntimeError('Failed to add block')
        self.pending_transactions = []
        return new_block

    def is_chain_valid(self, chain: List[Block] | None = None) -> bool:
        chain = chain or self.chain
        for i in range(1, len(chain)):
            current = chain[i]
            previous = chain[i - 1]
            if current.previous_hash != previous.hash:
                return False
            if current.compute_hash() != current.hash:
                return False
            if not current.hash.startswith('0' * self.difficulty):
                return False
        return True

    def get_chain_as_dict(self) -> List[Dict[str, Any]]:
        result = []
        for block in self.chain:
            result.append({
                'index': block.index,
                'timestamp': block.timestamp,
                'transactions': block.transactions,
                'previous_hash': block.previous_hash,
                'hash': block.hash,
                'nonce': block.nonce
            })
        return result

    def get_vehicle_history(self, vehicle_id: str) -> List[Dict[str, Any]]:
        history = []
        for block in self.chain:
            for tx in block.transactions:
                if tx.get('vehicle_id') == vehicle_id:
                    history.append({
                        'index': block.index,
                        'timestamp': block.timestamp,
                        'transaction': tx
                    })
        return history
```

---

## File: app.py

```python
# app.py
from flask import Flask, jsonify, request
from blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    tx_data = request.get_json()
    try:
        next_index = blockchain.add_new_transaction(tx_data)
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    return jsonify({'message': f'Transaction will be added to Block {next_index}.'}), 201

@app.route('/mine_block', methods=['GET'])
def mine_block():
    try:
        block = blockchain.mine()
    except RuntimeError as e:
        return jsonify({'message': str(e)}), 400
    response = {
        'message': 'New Block Forged',
        'index': block.index,
        'transactions': block.transactions,
        'timestamp': block.timestamp,
        'hash': block.hash,
        'previous_hash': block.previous_hash
    }
    return jsonify(response), 200

@app.route('/get_chain', methods=['GET'])
def get_chain():
    chain_data = blockchain.get_chain_as_dict()
    return jsonify({'length': len(chain_data), 'chain': chain_data}), 200

@app.route('/is_valid', methods=['GET'])
def is_valid():
    valid = blockchain.is_chain_valid()
    return jsonify({'is_valid': valid}), 200

@app.route('/vehicle_history/<vehicle_id>', methods=['GET'])
def vehicle_history(vehicle_id):
    history = blockchain.get_vehicle_history(vehicle_id)
    return jsonify({'vehicle_id': vehicle_id, 'history': history}), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
```

---

## File: tests/test\_blockchain.py

```python
# tests/test_blockchain.py
import pytest
from blockchain import Blockchain


def test_genesis_block():
    bc = Blockchain()
    assert len(bc.chain) == 1
    assert bc.chain[0].transactions[0]['transaction_type'] == 'genesis'


def test_add_transaction_and_mine():
    bc = Blockchain()
    tx = {
        'vehicle_id': 'MH12AB1234',
        'previous_owner': 'OwnerA',
        'new_owner': 'OwnerB',
        'price': 300000,
        'transaction_type': 'transfer'
    }
    idx = bc.add_new_transaction(tx)
    assert idx == 1
    block = bc.mine()
    assert len(bc.chain) == 2
    assert bc.chain[1].transactions[0]['vehicle_id'] == 'MH12AB1234'
    assert bc.is_chain_valid() is True


def test_vehicle_history():
    bc = Blockchain()
    tx1 = {
        'vehicle_id': 'MH14XY9999',
        'previous_owner': 'A',
        'new_owner': 'B',
        'price': 700000,
        'transaction_type': 'sale'
    }
    bc.add_new_transaction(tx1)
    bc.mine()
    hist = bc.get_vehicle_history('MH14XY9999')
    assert len(hist) == 1
    assert hist[0]['transaction']['new_owner'] == 'B'
```
