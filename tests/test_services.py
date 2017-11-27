
from io import BytesIO
import json
from unittest import TestCase, mock

import jwt

import app
from ddot_utils import ParseError

class DdotIngesterTestCase(TestCase):

    def setUp(self):
        app.application.config['JWT_SECRET_KEY'] = 'secret'
        app.application.config['JWT_PUBLIC_KEY'] = None
        app.application.config['JWT_ALGORITHM'] = 'HS256'
        app.application.config['AUTH_TOKEN_KEY_URL'] = ''
        app.application.config['JWT_DECODE_AUDIENCE'] = None
        app.application.testing = True
        self.app_client = app.application.test_client()


    def test_invalid_ddot_file(self):
        good_token = jwt.encode({'authorities': ['one_role', 'two_role']}, 'secret')
        with mock.patch('services.parse_ddot', side_effect=ParseError('Bad ddot file')):
            response = self.app_client.post('/ddots',
                                            content_type='multipart/form-data',
                                            headers={'Authorization': 'Bearer {0}'.format(good_token.decode('utf-8'))},
                                            data={'file': (BytesIO(b'Mocked ddot file'), 'ddot_file.txt')})
        self.assertEqual(response.status_code, 400)
        resp_data = json.loads(response.data)
        self.assertEqual({'error_message': 'Bad ddot file'}, resp_data)


    def test_valid_ddot_file(self):
        good_token = jwt.encode({'authorities': ['one_role', 'two_role']}, 'secret', algorithm='HS256')
        valid_result = [{
            'agencyCode' : 'USGS ',
            'siteNumber' : '480042108433301',
            'databaseTableIdentifier': '0',
            'transactionType': 'A',
            'stationName': 'YELLVILLE WATERWORKS'
            }]
        with mock.patch('services.parse_ddot', return_value=valid_result):
            response = self.app_client.post('/ddots',
                                            content_type='multipart/form-data',
                                            headers={'Authorization': 'Bearer {0}'.format(good_token.decode('utf-8'))},
                                            data={'file': (BytesIO(b'Mocked ddot file'),
                                                           'ddot_file.txt')})
        self.assertEqual(response.status_code, 200)
        resp_data = json.loads(response.data)
        self.assertEqual(len(resp_data), 1)
        self.assertEqual(valid_result[0], resp_data[0])

    def test_no_auth_header(self):
        good_token = jwt.encode({'authorities': ['one_role', 'two_role']}, 'secret', algorithm='HS256')
        valid_result = [{
            'agencyCode': 'USGS ',
            'siteNumber': '480042108433301',
            'databaseTableIdentifier': '0',
            'transactionType': 'A',
            'stationName': 'YELLVILLE WATERWORKS'
        }]
        with mock.patch('services.parse_ddot', return_value=valid_result):
            response = self.app_client.post('/ddots',
                                            content_type='multipart/form-data',
                                            data={'file': (BytesIO(b'Mocked ddot file'),
                                                           'ddot_file.txt')})
        self.assertEqual(response.status_code, 401)

    def test_bad_token(self):
        bad_token = jwt.encode({'authorities': ['one_role', 'two_role']}, 'bad_secret')
        valid_result = [{
            'agencyCode' : 'USGS ',
            'siteNumber' : '480042108433301',
            'databaseTableIdentifier': '0',
            'transactionType': 'A',
            'stationName': 'YELLVILLE WATERWORKS'
            }]
        with mock.patch('services.parse_ddot', return_value=valid_result):
            response = self.app_client.post('/ddots',
                                            content_type='multipart/form-data',
                                            headers={'Authorization': 'Bearer {0}'.format(bad_token.decode('utf-8'))},
                                            data={'file': (BytesIO(b'Mocked ddot file'),
                                                           'ddot_file.txt')})
        self.assertEqual(response.status_code, 422)

