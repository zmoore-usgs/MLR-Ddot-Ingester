
from io import BytesIO
import json
from unittest import TestCase, mock

import app
from ddot_utils import ParseError

class DdotIngesterTestCase(TestCase):

    def setUp(self):
        app.application.testing = True
        self.app_client = app.application.test_client()

    def test_invalid_ddot_file(self):
        with mock.patch('services.parse_ddot', side_effect=ParseError('Bad ddot file')):
            response = self.app_client.post('/ddots',
                                            content_type='multipart/form-data',
                                            data={'file': (BytesIO(b'Mocked ddot file'), 'ddot_file.txt')})
        self.assertEqual(response.status_code, 400)
        resp_data = json.loads(response.data)
        self.assertEqual({'error_message': 'Bad ddot file'}, resp_data)


    def test_valid_ddot_file(self):
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
                                            data={'file': (BytesIO(b'Mocked ddot file'),
                                                           'ddot_file.txt')})
        self.assertEqual(response.status_code, 200)
        resp_data = json.loads(response.data)
        self.assertEqual(len(resp_data), 1)
        self.assertEqual(valid_result[0], resp_data[0])


