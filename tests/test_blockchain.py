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
