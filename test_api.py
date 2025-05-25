import requests


def test_predict_ok():
    response = requests.post(
        "http://localhost:5000/predict",
        headers={
            "Content-Type": "application/json",
            "x-api-key": "supersecretkey123"
        },
        json={"features": [5.1, 3.5, 1.4, 0.2]}
    )
    assert response.status_code == 200
    assert "prediction" in response.json()


def test_predict_unauthorized():
    response = requests.post(
        "http://localhost:5000/predict",
        headers={"Content-Type": "application/json"},
        json={"features": [5.1, 3.5, 1.4, 0.2]}
    )
    assert response.status_code == 401
    