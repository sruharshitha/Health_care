from flask import Flask, jsonify
from flask_cors import CORS
from web3 import Web3
import ipfshttpclient

app = Flask(__name__)
CORS(app)

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

import ipfshttpclient

# connect to IPFS
ipfs = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')
ipfs._client._ignore_version = True

# contract address from sender laptop
contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"

abi = [
{
"inputs":[],
"name":"getCID",
"outputs":[{"internalType":"string","name":"","type":"string"}],
"stateMutability":"view",
"type":"function"
}
]

contract = w3.eth.contract(address=contract_address, abi=abi)

ipfs = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')

@app.route("/receive")
def receive():

    cid = contract.functions.getCID().call()

    data = ipfs.cat(cid)

    message = data.decode()

    return jsonify({
        "cid": cid,
        "message": message
    })


if __name__ == "__main__":
    print("Robot receiver running on port 6000")
    app.run(port=6000)