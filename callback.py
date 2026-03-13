import os
import logging
from flask import Flask, request, jsonify

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Server running", 200

@app.route("/callback", methods=["POST"])
def callback():
    # Safaricom M-Pesa callbacks come with JSON data
    data = request.get_json(silent=True)
    
    if data:
        logger.info("M-Pesa Callback Received: %s", data)
    else:
        logger.warning("Callback received with no JSON data")

    # Render/M-Pesa requirements: Always return valid JSON Accepted response
    return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"}), 200

@app.route("/telegram", methods=["POST"])
def telegram_webhook():
    # Telegram sends updates as JSON
    data = request.get_json(silent=True)
    
    if data:
        logger.info("Telegram Update Received: %s", data)
    else:
        logger.warning("Telegram request received with no JSON data")

    # Always return 200 OK to Telegram to avoid retries
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    # Render uses the PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    # Bind to 0.0.0.0 to be accessible externally
    app.run(host="0.0.0.0", port=port)
