import pytest
import json
from app import app  # Importer l'application Flask
import sys
import os

# Ajouter le chemin du projet à sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))




@pytest.fixture
def client():
    """Client de test pour l'application Flask."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_prediction_success(client):
    """Test d'une requête valide à l'API de prédiction."""
    data = {
        "age": 60, "anaemia": 0, "creatinine_phosphokinase": 150,
        "diabetes": 1, "ejection_fraction": 35, "high_blood_pressure": 0,
        "platelets": 250000, "serum_creatinine": 1.2, "serum_sodium": 140,
        "sex": 1, "smoking": 0, "time": 4
    }
    response = client.post('/main/api/make_prediction', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    json_data = response.get_json()
    assert "prediction" in json_data

def test_missing_feature(client):
    """Test d'une requête avec une feature manquante."""
    data = {
        "age": 60, "anaemia": 0, "diabetes": 1  # Manque des colonnes
    }
    response = client.post('/main/api/make_prediction', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    json_data = response.get_json()
    assert "error" in json_data
