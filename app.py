import os
import logging
from flask import Flask, request, jsonify
import joblib
import numpy as np
from functools import wraps


if not os.path.exists("logs"):
    os.makedirs("logs")


API_KEY = "supersecretkey123"


def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get("x-api-key")
        if key and key == API_KEY:
            return f(*args, **kwargs)
        else:
            logging.warning(f"unauthorized access attempt from {request.remote_addr}")
            return jsonify({"error": "unauthorized"}), 401
    return decorated


logging.basicConfig(
    filename='logs/access.log',
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s'
)


# Load model
model = joblib.load("model.joblib")

# Init flask
app = Flask(__name__)


@app.before_request
def log_request_info():
    ip = request.remote_addr
    path = request.path
    method = request.method
    logging.info(f"{ip} called {method} {path}")


# Predict route
@app.route("/predict", methods=["POST"])
@require_api_key
def predict():
    data = request.get_json()
    if not data or "features" not in data:
        return jsonify({"error": "Invalid input format"}), 400

    try:
        features = np.array(data["features"]).reshape(1, -1)
        prediction = model.predict(features)
        return jsonify({"prediction": int(prediction[0])})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Start app
if __name__ == "__main__":
    app.run(port=5000, debug=True)
