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
