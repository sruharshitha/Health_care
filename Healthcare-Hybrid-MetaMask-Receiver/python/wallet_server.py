from flask import Flask, request

app = Flask(__name__)

@app.route("/wallet", methods=["POST"])
def save_wallet():

    wallet = request.json["wallet"]

    with open("wallet.txt","w") as f:
        f.write(wallet)

    return {"status":"saved"}

if __name__ == "__main__":
    app.run(port=5002)