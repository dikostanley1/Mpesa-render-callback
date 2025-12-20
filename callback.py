from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/callback", methods=["POST"])
def callback():
    data = request.json
    print("CALLBACK RECEIVED:", data)
    return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})
