import pytest
import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app


@pytest.fixture
def client():
    """Test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_homepage(client):
    """Test that the homepage loads correctly."""
    response = client.get('/')
    assert response.status_code == 200


def test_prediction_success(client):
    """Test a valid prediction request to the API."""
    data = {
        "age": 60, "anaemia": 0, "creatinine_phosphokinase": 150,
        "diabetes": 1, "ejection_fraction": 35, "high_blood_pressure": 0,
        "platelets": 250000, "serum_creatinine": 1.2, "serum_sodium": 140,
        "sex": 1, "smoking": 0, "time": 4
    }
    response = client.post(
        '/main/api/make_prediction',
        data=json.dumps(data),
        content_type='application/json'
    )
    assert response.status_code == 200
    json_data = response.get_json()
    assert "prediction" in json_data


def test_missing_feature(client):
    """Test a request with missing features returns 400."""
    data = {
        "age": 60, "anaemia": 0, "diabetes": 1
    }
    response = client.post(
        '/main/api/make_prediction',
        data=json.dumps(data),
        content_type='application/json'
    )
    assert response.status_code == 400
    json_data = response.get_json()
    assert "error" in json_data
