import unittest
from flask import Flask
# Replace with your actual Flask app file
from routes.predict import predict_routes


class FlaskRoutesTestCase(unittest.TestCase):
    # Set up the Flask test client
    def setUp(self):
        self.app = Flask(__name__)
        predict_routes(self.app)
        self.client = self.app.test_client()

    # Test the health check route
    def test_health_check(self):
        response = self.client.get('/health_check')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'health_check': True})

    # Test the predict route if one field is missing
    def test_predict_missing_field(self):
        form_data = {'PRG': '100', 'PL': '150', 'PR': '120', 'SK': '130', 'TS': '140',
                    'M11': '160', 'BD2': '170', 'Age': '30'}
        response = self.client.post('/predict/patient', data=form_data)
        assert response.status_code == 400
        assert response.get_json() == {'error': 'Le champ Insurance est obligatoire.'}

    # Test the predict route if one field is invalid (string instead of int)
    def test_predict_invalid_field_value(self):
        form_data = {'PRG': '100', 'PL': '150', 'PR': '120', 'SK': '130', 'TS': '140',
                    'M11': '160', 'BD2': '170', 'Age': '30', 'Insurance': 'string'}
        response = self.client.post('/predict/patient', data=form_data)
        assert response.status_code == 400
        assert response.get_json() == {'error': 'La valeur du champ Insurance doit être un entier.'}

    # Test the predict route if all fields are valid
    def test_predict(self):
        form_data = {'PRG': '100', 'PL': '150', 'PR': '120', 'SK': '130', 'TS': '140',
                    'M11': '160', 'BD2': '170', 'Age': '30', 'Insurance': '200'}
        response = self.client.post('/predict/patient', data=form_data)
        assert response.status_code == 200
        response_json = response.get_json()
        assert 'prediction' in response_json
        assert response_json['form_data'] == form_data