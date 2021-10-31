import functools
import json
import pickle
import requests

from utility.hash_util import hash_block
from utility.verification import Verification
from utility.printable import Printable
from transaction import Transaction
from block import Block
from wallet import Wallet

# The reward we give our miners for creating a new block
MINING_REWARD = 10

class Blockchain:
    def __init__(self, public_key, node_id):
        # Starting block for the blockchain
        genesis_block = Block(0, '', [], 100, 0)
        # Initizalize the blockchain
        self.chain = [genesis_block]
        # Unhandled transactions
        self.__open_transactions = []
        # Load the data

        self.public_key = public_key
        self.__peer_nodes = set()
        self.node_id = node_id
        self.resolve_conflicts = False
        self.load_data()

    def get_chain(self):
        return self.chain[:]
    
    def get_open_transactions(self):
        return self.__open_transactions[:]

    def load_data(self):
        try:
            with open(f'blockchain-{self.node_id}.txt', mode='r') as f:
                # file_content = pickle.loads(f.read())
                file_content = f.readlines()
                # blockchain = file_content['chain']
                # open_transactions = file_content['ot']
                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(
                        tx['sender'], 
                        tx['recipient'], 
                        tx['amount'], 
                        tx['signature'])
                    for tx in block['transactions']]
                    updated_block = Block(
                        block['index'],
                        block['previous_hash'],
                        converted_tx,
                        block['proof'],
                        block['timestamp']
                    )
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain
                self.__open_transactions = json.loads(file_content[1][:-1])
                updated_transactions = []
                for tx in self.__open_transactions:
                    updated_transaction = Transaction(
                        tx['sender'],
                        tx['recipient'],
                        tx['amount'],
                        tx['signature']
                    )
                    updated_transactions.append(updated_transaction)
                self.__open_transactions = updated_transactions
                peer_nodes = json.loads(file_content[2])
                self.__peer_nodes = set(peer_nodes)
        except (IOError, IndexError):
            pass
        finally:
            print('Cleanup.')

    def save_data(self):
        try:
            with open(f'blockchain-{self.node_id}.txt', mode='w') as f:
                saveable_chain = [block.__dict__ for block in [Block(
                    block_el.index,
                    block_el.previous_hash,
                    [tx.__dict__ for tx in block_el.transactions],
                    block_el.proof,
                    block_el.timestamp
                ) for block_el in self.chain]]
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(saveable_tx))
                f.write('\n')
                f.write(json.dumps(list(self.__peer_nodes)))
                # data = {
                #     'chain': blockchain,
                #     'ot': open_transactions
                # }
                # f.write(pickle.dumps(data))
        except IOError:
            print('Saving failed.')

    def proof_of_work(self):
        last_block = self.chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1
        return proof


    def get_balance(self, sender=None):
        """Calculate and return the balance for a participant.

        Arguments:
            :participant: The person for whom to calculate the balance.
        """
        if sender == None:
            if self.public_key == None:
                return None
            participant = self.public_key
        else:
            participant = sender
        tx_sender = [[tx.amount for tx in block.transactions 
            if tx.sender == participant] 
            for block in self.chain]
        open_tx_sender = [tx.amount for tx in self.__open_transactions 
            if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        amount_sent = functools.reduce(
            lambda tx_sum, tx_amt: 
            tx_sum + sum(tx_amt) 
            if len(tx_amt) > 0 
            else tx_sum + 0, tx_sender, 0
        )
        tx_recipient = [[tx.amount for tx in block.transactions 
            if tx.recipient == participant]
            for block in self.chain
        ]
        amount_received = functools.reduce(
            lambda tx_sum, tx_amt: 
            tx_sum + sum(tx_amt) 
            if len(tx_amt) > 0 
            else tx_sum + 0, tx_recipient, 0
        )
        return amount_received - amount_sent


    def get_last_blockchain_value(self):
        """Returns the last value of the current blockchain."""
        if len(self.chain) < 1:
            return None
        return(self.chain[-1])


    def add_transaction(self, sender, recipient, amount, signature, is_receiving=False):
        """Append a new value as well as the last blockchain value to the blockchain.

        Arguments:
            :sender: The sender of the coins
            :recipient: The recipient of the coins
            :amount: The amount of coins sent with the transaction (default 1.0 coins)
            :is_receiving: Whether or not the node is receiving transactions.   
        """
        # transaction = {
        #     'sender': sender,
        #     'recipient': recipient,
        #     'amount': amount
        # }
        if self.public_key == None:
            return False
        transaction = Transaction(sender, recipient, amount, signature)
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction) 
            self.save_data()
            if not is_receiving:
                for peer_node in self.__peer_nodes:
                    url = f'http://{peer_node}/broadcast-transaction'
                    try:
                        response = requests.post(url, json={
                            'sender': sender, 
                            'recipient': recipient, 
                            'amount': amount, 
                            'signature': signature
                        })
                        if response.status_code == 400 or response.status_code == 500:
                            print('Transaction declined, needs resolving.')
                            return False
                    except requests.exceptions.ConnectionError:
                        continue
            return True
        return False

    def mine_block(self):
        """Mines a block (appends all open transactions to the blockchain as a block)."""
        if self.public_key == None:
            return None        
        # Fetch the currently last block of the blockchain
        last_block = self.chain[-1]
        # Hash the last block (to be able to compare it to the stored has value)
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        # Miners should be rewarded, so let's create a reward transaction
        # reward_transaction = {
        #     'sender': 'MINING',
        #     'recipient': owner,
        #     'amount': MINING_REWARD
        # }
        reward_transaction = Transaction('MINING', self.public_key, MINING_REWARD, '')
        # Copy transaction instead of manipulating the original open_transactions
        # This ensures that if for some reason the mining would fail, we don't mess up
        copied_transactions = self.__open_transactions[:]
        for tx in copied_transactions:
            if not Wallet.verify_transaction(tx):
                return None
        copied_transactions.append(reward_transaction)
        block = Block(
            len(self.chain), 
            hashed_block, 
            copied_transactions, 
            proof
        )
        self.chain.append(block)
        self.__open_transactions = []
        self.save_data()

        converted_block = block.__dict__.copy()
        converted_block['transactions'] = [tx.__dict__ for tx in converted_block['transactions']]

        for node in self.__peer_nodes:
            url = f'http://{node}/broadcast-block'
            try:
                response = requests.post(url, json={'block': converted_block})
                if response.status_code == 400 or response.status_code == 500:
                    print('Transaction declined, needs resolving.')
                if response.status_code == 409:
                    self.resolve_conflicts = True
            except requests.exceptions.ConnectionError:
                continue
        return block
    
    def add_block(self, block):
        """Adds a new block."""
        transactions = [Transaction(tx['sender'], tx['recipient'], tx['amount'], tx['signature']) for tx in block['transactions']]
        proof_is_valid = Verification.valid_proof(transactions[:-1], block['previous_hash'], block['proof'])
        hashes_match = hash_block(self.chain[-1]) == block['previous_hash']
        if not proof_is_valid or not hashes_match:
            return False
        converted_block = Block(
            block['index'], 
            block['previous_hash'], 
            transactions, 
            block['proof'], 
            block['timestamp']
        )
        self.chain.append(converted_block)
        stored_transactions = self.__open_transactions[:]
        for itx in block['transactions']:
            for opentx in stored_transactions:
                if opentx.sender == itx['sender'] and opentx.recipient == itx['recipient'] and opentx.amount == itx['amount'] and opentx.signature == itx['signature']:
                    try:
                        self.__open_transactions.remove(opentx)
                    except ValueError:
                        print('Item was already removed.')
        self.save_data()
        return True

    def resolve(self):
        winner_chain = self.chain
        replace = False
        for node in self.__peer_nodes:
            url = f'http://{node}/chain'
            try:
                response = requests.get(url)
                node_chain = response.json()
                node_chain = [Block(
                    block['index'], 
                    block['previous_hash'],
                    [Transaction(
                        tx['sender'],
                        tx['recipient'],
                        tx['amount'],
                        tx['signature']
                    ) for tx in block['transactions']],
                    block['proof'],
                    block['timestamp']
                ) for block in node_chain]
                node_chain_length = len(node_chain)
                local_chain_length = len(winner_chain)
                if node_chain_length > local_chain_length and Verification.verify_chain(node_chain):
                    winner_chain = node_chain
                    replace = True
            except requests.exceptions.ConnectionError:
                continue
        self.resolve_conflicts = False
        self.chain = winner_chain
        if replace:
            self.__open_transactions = []
        self.save_data()
        return replace

    def add_peer_node(self, node):
        """Adds a new node to the new peer node set.

        Arguments:
            :node: the node URL which should be added.
        """
        self.__peer_nodes.add(node)
        self.save_data()

    def remove_peer_node(self, node):
        """Removes a node from the peer node set.

        Arguments:
            :node: the node URL which should be removed.
        """
        self.__peer_nodes.discard(node)
        self.save_data()

    def get_peer_nodes(self):
        """Returns a list of all connected peer nodes."""
        return list(self.__peer_nodes)