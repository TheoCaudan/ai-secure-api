# Mini Project: Securing an AI API with Flask

## Overview

This project demonstrates how to build a simple yet secure REST API in Python using Flask that serves predictions from a pre-trained machine learning model (Random Forest trained on the Iris dataset). The main focus is on API security through API key authentication.

The API accepts feature data via POST requests, runs predictions using the pre-trained model, and returns the predicted class. It also logs all access attempts, including unauthorized ones.

---

## Features

- **AI Model**: Pre-trained Random Forest classifier using the Iris dataset (saved as `model.joblib`).
- **Flask REST API** exposing a `/predict` endpoint.
- **API Key authentication** via the `x-api-key` HTTP header.
- **Request logging** with timestamps, IP addresses, and request details.
- **Robust error handling** for invalid inputs and internal errors.

---

## Project Structure

```
.
├── app.py                 # Main Flask API code
├── model.joblib           # Pre-trained ML model saved with joblib
├── logs/
│   └── access.log         # Log file for API requests
└── README.md              # This README file
```

---

## Prerequisites

- Python 3.7 or higher
- Required Python packages:
  - Flask
  - scikit-learn
  - joblib
  - numpy

Install dependencies with:

```bash
pip install flask scikit-learn joblib numpy
```

---

## Usage

### 1. Ensure `model.joblib` is Available

The API relies on a pre-trained model file named `model.joblib`. Ensure this file is present in the project root. If not provided, you can generate it locally using a training script (see "Customization" section for details), but this is not required for the current workflow.

---

### 2. Start the Flask Server (Development)

For development, run the Flask app locally with debugging enabled:

```bash
export FLASK_ENV=development
python app.py
```

The API will be available at:

```
http://127.0.0.1:5000
```

**Note**: For production, the app uses gunicorn (see Docker instructions below). Do not use `debug=True` in production as it poses a security risk.

---

### 3. Make a Prediction Request

Use `curl`, `Postman`, or any HTTP client to test the `/predict` endpoint:

```bash
curl -X POST http://127.0.0.1:5000/predict   -H "Content-Type: application/json"   -H "x-api-key: supersecretkey123"   -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

Sample response:

```json
{
  "prediction": 0
}
```

---

## Security

- The `/predict` endpoint is protected by a static API key.
- Set your API key by editing the `API_KEY` variable in `app.py`.
- Requests with missing or incorrect keys return:

```json
{
  "error": "unauthorized"
}
```

- All unauthorized access attempts are logged with source IP and timestamp.

---

## Logging

- Logs are saved in the `logs/access.log` file.
- Each request logs:
  - Timestamp
  - IP address
  - HTTP method
  - Endpoint path
- Unauthorized attempts trigger a warning-level log.

---

## Customization

- Change the API key by editing this line in `app.py`:

```python
API_KEY = "your_new_key_here"
```

- Replace `model.joblib` with any other pre-trained model that matches the expected input shape (4 features for the Iris dataset).
- To generate `model.joblib` locally (if needed), you can use a training script. For example, create a `train_model.py` with:

```python
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load and train model
iris = load_iris()
model = RandomForestClassifier()
model.fit(iris.data, iris.target)

# Save model
joblib.dump(model, 'model.joblib')
```

Then run `python train_model.py` to create the file.

- Add more endpoints using the same `@require_api_key` decorator to secure them.

---

## Conclusion

This mini-project is a hands-on example of how to serve a pre-trained ML model securely through a REST API using Flask. It shows how to:
- Implement API key protection,
- Monitor access through logging,
- Handle JSON input and output cleanly,
- Prepare for real-world deployment needs.

---

## Optional Next Steps

- Add HTTPS support using a reverse proxy (e.g., Nginx + certbot).
- Add rate-limiting with Flask-Limiter.
- Containerize with Docker.
- Deploy to the cloud (e.g., AWS, Heroku, Railway).

Let me know if you want help generating a `Dockerfile` or `requirements.txt`!

---

## Docker Support

You can run this project in a container using Docker. The container uses gunicorn for production-grade deployment.

### 1. Build the Docker Image

```bash
docker build -t secure-ml-api .
```

### 2. Run the Container

```bash
docker run -p 5000:5000 secure-ml-api
```

The API will be available at `http://localhost:5000`.

### Dockerfile

The Dockerfile uses gunicorn to serve the app in production:

```dockerfile
FROM python:3.10-slim-bookworm

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
```

### .dockerignore

To improve build efficiency and reduce image size, make sure you include a `.dockerignore` file. Here's a recommended example:

```
__pycache__/
*.pyc
*.pyo
*.pyd
*.db
*.sqlite3
*.log
*.joblib
venv/
.env
logs/
```
