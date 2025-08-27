# blockchain.py
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
