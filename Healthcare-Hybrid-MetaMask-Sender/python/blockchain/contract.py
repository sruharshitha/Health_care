from web3 import Web3
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# -------------------------
# CONNECT TO BLOCKCHAIN
# -------------------------
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

if not web3.is_connected():
    print("⚠ Web3 not connected. Blockchain features disabled.")

# -------------------------
# LOAD CONTRACT
# -------------------------
with open(os.path.join(BASE_DIR, "contract.json")) as f:
    contract_json = json.load(f)

# ✅ FIX: convert contract address to checksum
contract_address = Web3.to_checksum_address(contract_json["address"])

contract = web3.eth.contract(
    address=contract_address,
    abi=contract_json["abi"]
)

# -------------------------
# STORE MESSAGE
# -------------------------
def store_message(cid, sender, token):
    try:
        # ✅ FIX: convert sender to checksum
        sender_address = Web3.to_checksum_address(sender)

        # Use first Hardhat account (also checksum)
        from_account = Web3.to_checksum_address(web3.eth.accounts[0])

        tx = contract.functions.storeMessage(
            cid,
            sender_address,
            token
        ).transact({
            'from': from_account
        })

        receipt = web3.eth.wait_for_transaction_receipt(tx)
        block = web3.eth.get_block(receipt.blockNumber)

        print("\n====== BLOCKCHAIN TRANSACTION ======")
        print("CID:", cid)
        print("Doctor Wallet:", sender_address)
        print("Session Token:", token)
        print("Block Number:", receipt.blockNumber)
        print("Gas Used:", receipt.gasUsed)
        print("Timestamp:", block.timestamp)
        print("===================================\n")

        return receipt

    except Exception as e:
        print("❌ Blockchain Error:", e)
        return None


# -------------------------
# GET MESSAGE COUNT
# -------------------------
def get_message_count():
    try:
        return contract.functions.messagesLength().call()
    except Exception as e:
        print("❌ Error getting message count:", e)
        return 0


# -------------------------
# GET MESSAGE INFO
# -------------------------
def get_message_info(index):
    try:
        msg = contract.functions.messages(index).call()
        return msg[0], msg[1], msg[2]
    except Exception as e:
        print("❌ Error getting message info:", e)
        return None