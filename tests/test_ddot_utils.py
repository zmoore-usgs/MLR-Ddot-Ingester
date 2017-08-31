
from unittest import TestCase

from ddot_utils import get_transactions, parse_key_value_pairs, ParseError, parse

class GetTransactionsTestCase(TestCase):

    def setUp(self):
        self.location1 = [
            'USGS 480042108433301 R=0* T=A* 12=\'YELLVILLE WATERWORKS\'* 11=S* 35=M* 36=NAD27*',
            'USGS 480042108433301 6=05* 7=05* 8=089* 20=11010003* 802=NNNNNNNNNNNNYNNNNNNN*',
            'USGS 480042108433301 39=WS* 813=CST* 814=Y* 3=C* 41=US*'
        ]
        self.location2 = [
            'USEPA123456789012345 R=0* T=A* 12=\'INTAKE ON LAKE WOBEGON\'* 802=FA-DV',
            'USEPA123456789012345 Long Line S* 35=M* 36=NAD27* 6=05* 7=05* 8=023* 20=11010014*'
        ]

        self.location3 = ['USGS 580042108433301']

    def test_no_locations(self):
        self.assertEqual(get_transactions([]), [])

    def test_no_key_value_pairs_location(self):
        result = get_transactions(self.location3)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].get('agencyCode'), 'USGS ')
        self.assertEqual(result[0].get('siteNumber'), '580042108433301')
        self.assertEqual(result[0].get('key_value_pairs'), '')
        self.assertEqual(result[0].get('line_numbers'), [2])

    def test_single_location(self):
        result = get_transactions(self.location1)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].get('agencyCode'), 'USGS ')
        self.assertEqual(result[0].get('siteNumber'), '480042108433301')
        self.assertEqual(result[0].get('key_value_pairs'),
                         ('R=0* T=A* 12=\'YELLVILLE WATERWORKS\'* 11=S* 35=M* 36=NAD27* '
                          '6=05* 7=05* 8=089* 20=11010003* 802=NNNNNNNNNNNNYNNNNNNN* '
                          '39=WS* 813=CST* 814=Y* 3=C* 41=US*')
                         ),
        self.assertEqual(result[0].get('line_numbers'), [2, 3, 4])

    def test_two_locations(self):
        result = get_transactions(self.location1 + self.location2)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].get('agencyCode'), 'USGS ')
        self.assertEqual(result[0].get('siteNumber'), '480042108433301')
        self.assertEqual(result[0].get('key_value_pairs'),
                         ('R=0* T=A* 12=\'YELLVILLE WATERWORKS\'* 11=S* 35=M* 36=NAD27* '
                          '6=05* 7=05* 8=089* 20=11010003* 802=NNNNNNNNNNNNYNNNNNNN* '
                          '39=WS* 813=CST* 814=Y* 3=C* 41=US*')
                         )
        self.assertEqual(result[0].get('line_numbers'), [2, 3, 4])

        self.assertEqual(result[1].get('agencyCode'), 'USEPA')
        self.assertEqual(result[1].get('siteNumber'), '123456789012345')
        self.assertEqual(result[1].get('key_value_pairs'),
                         ('R=0* T=A* 12=\'INTAKE ON LAKE WOBEGON\'* 802=FA-DV '
                          'Long Line S* 35=M* 36=NAD27* 6=05* 7=05* 8=023* 20=11010014*')
                         )
        self.assertEqual(result[1].get('line_numbers'), [5, 6])


class ParseKeyValuePairsTestCase(TestCase):

    def test_with_empty_string(self):
        with self.assertRaises(ParseError):
            parse_key_value_pairs('')

    def test_with_single_key_value_pair(self):
        self.assertEqual(parse_key_value_pairs('12=Test*'), [('12', 'Test')])
        self.assertEqual(parse_key_value_pairs('13#Another test$'), [('13', 'Another test')])

    def test_with_multiple_key_value_pairs(self):
        self.assertEqual(parse_key_value_pairs(
            '12=Test* 13#Another test$'),
            [('12', 'Test'), ('13', 'Another test')])

    def test_with_incomplete_key_value_pair(self):
        with self.assertRaises(ParseError) as e:
            parse_key_value_pairs('12=Test* 13')
        self.assertIn('13', e.exception.message)

        with self.assertRaises(ParseError) as e:
            parse_key_value_pairs('12=Test* 13=This')
        self.assertIn('13=This', e.exception.message)


class ParseTestCase(TestCase):

    def setUp(self):
        self.maxDiff = None

        self.location1_transaction_start = 'USGS 480042108433301 R=0* T=A*'
        self.location1 = (
            'USGS 480042108433301 R=0* T=A* 12=\'YELLVILLE WATERWORKS\'* 11=S* 35=M* 36=NAD27*\n'
            'USGS 480042108433301 6=05* 7=05* 8=089* 20=11010003* 802=NNNNNNNNNNNNYNNNNNNN*\n'
            'USGS 480042108433301 39=WS* 813=CST* 814=Y* 3=C* 41=US*'
        )
        self.location2 = (
            'USEPA123456789012345 R=0* T=A* 12=\'INTAKE ON LAKE WOBEGON\'* 802=FA-DV\n'
            'USEPA123456789012345 Long Line* 35=M* 36=NAD27* 6=05* 7=05* 8=023* 20=11010014*'
        )

        self.location3 = (
            'USGS 580042108433301 R=0* T=A*\n'
            'USGS 580042108433301 12'
        )

        self.long_line = (
            'USGS 480042108433301 R=0* T=A* 12=\'YELLVILLE WATERWORKS JUNK JUNK JUNK JUNK STUFF STUFF STUFF STUFF\'* 11=S* 35=M* 36=NAD27*\n'
            'USGS 480042108433301 39=WS* 813=CST* 814=Y* 3=C* 41=US*'
        )

    def test_no_contents(self):
        with self.assertRaises(ParseError):
            parse('')

    def test_with_no_transactions(self):
        with self.assertRaises(ParseError):
            parse('XXXXXXXX')

    def test_with_line_too_long(self):
        with self.assertRaises(ParseError) as e:
            parse('XXXXXXX\n' + self.long_line)
        self.assertIn('line 2', e.exception.message)

    def test_with_single_location(self):
        result = parse('XXXXXXX\n' +self.location1)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], {
            'agencyCode': 'USGS ',
            'siteNumber': '480042108433301',
            'databaseTableIdentifier': '0',
            'transactionType': 'A',
            'stationName': 'YELLVILLE WATERWORKS',
            'coordinateAccuracyCode': 'S',
            'coordinateMethodCode': 'M',
            'coordinateDatumCode': 'NAD27',
            'districtCode': '05',
            'stateFipsCode': '05',
            'countyCode': '089',
            'hydrologicUnitCode': '11010003',
            'siteTypeCode': 'NNNNNNNNNNNNYNNNNNNN',
            'nationalWaterUseCode': 'WS',
            'timeZoneCode': 'CST',
            'daylightSavingsTimeFlag': 'Y',
            'dataReliabilityCode': 'C',
            'countryCode': 'US'
        })

    def test_with_two_locations(self):
        result = parse('XXXXXXX\n' + self.location1 + '\n' + self.location2)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], {
            'agencyCode': 'USGS ',
            'siteNumber': '480042108433301',
            'databaseTableIdentifier': '0',
            'transactionType': 'A',
            'stationName': 'YELLVILLE WATERWORKS',
            'coordinateAccuracyCode': 'S',
            'coordinateMethodCode': 'M',
            'coordinateDatumCode': 'NAD27',
            'districtCode': '05',
            'stateFipsCode': '05',
            'countyCode': '089',
            'hydrologicUnitCode': '11010003',
            'siteTypeCode': 'NNNNNNNNNNNNYNNNNNNN',
            'nationalWaterUseCode': 'WS',
            'timeZoneCode': 'CST',
            'daylightSavingsTimeFlag': 'Y',
            'dataReliabilityCode': 'C',
            'countryCode': 'US'
        })
        self.assertEqual(result[1], {
            'agencyCode': 'USEPA',
            'siteNumber': '123456789012345',
            'databaseTableIdentifier': '0',
            'transactionType': 'A',
            'stationName': 'INTAKE ON LAKE WOBEGON',
            'siteTypeCode': 'FA-DV Long Line',
            'coordinateMethodCode': 'M',
            'coordinateDatumCode': 'NAD27',
            'districtCode': '05',
            'stateFipsCode': '05',
            'countyCode': '023',
            'hydrologicUnitCode': '11010014'
        })

    def test_with_no_code_separator(self):
        with self.assertRaises(ParseError) as err:
            result = parse('XXXXXX\n' + self.location1 + '\n' + self.location3)
        self.assertIn('[5, 6]', err.exception.message)
        self.assertIn('12', err.exception.message)

    def test_with_no_value_ending_token(self):
        with self.assertRaises(ParseError) as err:
            result = parse('XXXXXX\n' + self.location1 + '\n' + self.location3 + '=13')
        self.assertIn('[5, 6]', err.exception.message)
        self.assertIn('12=13', err.exception.message)

    def test_with_duplicate_station_name(self):
        with self.assertRaises(ParseError) as err:
            result = parse('XXXXXX\n' + self.location1 + '\n' + 'USGS 480042108433301 900=Another name*')
        self.assertIn('2, 3, 4, 5', err.exception.message)
        self.assertIn('Duplicate station name', err.exception.message)

    def test_with_trailing_quote_and_no_starting_quote_on_station_name(self):
        result = parse('XXXXXX\n' +
                       self.location1_transaction_start +
                       ' 12=\'YELLVILLE WATERWORKS*'
        )
        self.assertEqual(result[0].get('stationName'), '\'YELLVILLE WATERWORKS')

    def test_with_starting_quote_and_no_ending_quote_on_station_name(self):
        result = parse('XXXXXX\n' +
                       self.location1_transaction_start +
                       ' 12=YELLVILLE WATERWORKS\'*'
        )
        self.assertEqual(result[0].get('stationName'), 'YELLVILLE WATERWORKS\'')

    def test_with_unknown_code(self):
        result = parse('XXXXX\n' + self.location2 + '\n' + 'USEPA123456789012345 ZZ=13*')
        self.assertEqual(result[0], {
            'agencyCode': 'USEPA',
            'siteNumber': '123456789012345',
            'databaseTableIdentifier': '0',
            'transactionType': 'A',
            'stationName': 'INTAKE ON LAKE WOBEGON',
            'siteTypeCode': 'FA-DV Long Line',
            'coordinateMethodCode': 'M',
            'coordinateDatumCode': 'NAD27',
            'districtCode': '05',
            'stateFipsCode': '05',
            'countyCode': '023',
            'hydrologicUnitCode': '11010014'
        })