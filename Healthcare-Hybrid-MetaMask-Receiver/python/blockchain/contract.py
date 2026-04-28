from web3 import Web3
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

web3 = Web3(Web3.HTTPProvider("http://10.10.222.130:8545"))

with open(os.path.join(BASE_DIR, "contract.json")) as f:
    contract_json = json.load(f)

contract = web3.eth.contract(
    address=contract_json["address"],
    abi=contract_json["abi"]
)

def store_message(cid, sender, token):
    tx = contract.functions.storeMessage(cid, sender, token).transact({
        'from': web3.eth.accounts[0]
    })

    receipt = web3.eth.wait_for_transaction_receipt(tx)
    block = web3.eth.get_block(receipt.blockNumber)

    print("\n====== BLOCKCHAIN TRANSACTION ======")
    print("CID:", cid)
    print("Doctor Wallet:", sender)
    print("Session Token:", token)
    print("Block Number:", receipt.blockNumber)
    print("Gas Used:", receipt.gasUsed)
    print("Timestamp:", block.timestamp)
    print("===================================\n")

    return receipt


def get_message_count():
    return contract.functions.messagesLength().call()


def get_message_info(index):
    msg = contract.functions.messages(index).call()
    return msg[0], msg[1], msg[2]