import sys
import os
import pandas as pd

# Ensure src/ directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api_routes import preprocess_input


def test_preprocess_input():
    """Verify that preprocess_input correctly transforms the data."""
    form_data = {
        "age": 60, "anaemia": 0, "creatinine_phosphokinase": 150,
        "diabetes": 1, "ejection_fraction": 35, "high_blood_pressure": 0,
        "platelets": 250000, "serum_creatinine": 1.2, "serum_sodium": 140,
        "sex": 1, "smoking": 0, "time": 4
    }
    processed_data = preprocess_input(form_data)

    assert isinstance(processed_data, pd.DataFrame)
    assert list(processed_data.columns) == [
        'age', 'anaemia', 'creatinine_phosphokinase',
        'diabetes', 'ejection_fraction', 'high_blood_pressure',
        'platelets', 'serum_creatinine', 'serum_sodium',
        'sex', 'smoking', 'time'
    ]
