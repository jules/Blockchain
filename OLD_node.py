from uuid import uuid4
from blockchain import Blockchain
from utility.verification import Verification
from wallet import Wallet


class Node:
    def __init__(self):
        # self.wallet.public_key = str(uuid4())
        self.wallet = Wallet()
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)

    def get_transaction_value(self):
        """Returns the input of the user (the recipient of the new transaction and an amount) as a tuple."""
        tx_recipient = input('Enter the recipient of the transaction:')
        tx_amount = float(input('Your transaction amount please: '))
        return (tx_recipient, tx_amount)

    def get_user_choice(self):
        """Returns the input of the user to choose an option in the user interface."""
        user_input = input('Input your choice: ')
        return user_input

    def print_blockchain_blocks(self):
        for block in self.blockchain.get_chain():
            print('Outputting Block')
            print(f'{block}\n')
        else:
            print('-' * 20)

    def listen_for_input(self):
        waiting_for_input = True
        while waiting_for_input:
            print('Please choose:')
            print('1: Add a new transaction value')
            print('2: Mine a new block')
            print('3: Output the blockchain blocks')
            print('4: Check transaction validity')
            print('5: Create wallet')
            print('6: Load wallet')
            print('7: Save keys')
            print('q: Quit')
            user_choice = self.get_user_choice()
            if user_choice == '1':
                # Query the user for a transaction input and add the value to the blockchain
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data
                signature = self.wallet.sign_transaction(self.wallet.public_key, recipient, amount)
                if self.blockchain.add_transaction(self.wallet.public_key, recipient, amount, signature):
                    print('Added transaction.')
                else:
                    print('Transaction failed.')
            elif user_choice == '2':
                if not self.blockchain.mine_block():
                    print('Mining failed.')
            elif user_choice == '3':
                # Output the blockchain to the console
                self.print_blockchain_blocks()
            elif user_choice == '4':
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print('All transactions are valid.')
                else:
                    print('There are invalid transactions.')
            elif user_choice == '5':
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
                print('Wallet created.')
            elif user_choice == '6':
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
                print('Wallet loaded.')
            elif user_choice == '7':
                self.wallet.save_keys()
                print('Keys saved.')
            elif user_choice == 'q':
                # Quit the loop
                print('Quitting...')
                waiting_for_input = False
            else:
                print('Input was invalid, please pick value from the list.')
            if not Verification.verify_chain(self.blockchain.get_chain()):
                # print_blockchain_blocks()
                print('Invalid blockchain.')
                waiting_for_input = False
            print('Balance of {}: {:6.2f}'.format(
                self.wallet.public_key, self.blockchain.get_balance()))
        print('Done!')


if __name__ == '__main__':
    home_node = Node()
    home_node.listen_for_input()
