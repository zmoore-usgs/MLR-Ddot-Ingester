
from unittest import TestCase

from ddot_utils import get_transactions, parse_key_value_pairs, validate_lines, ParseError, parse

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

class ValidateLinesTestCase(TestCase):
    def setUp(self):
        self.maxDiff = None

        self.location1 = [
            'USGS 480042108433301 R=0* T=A* 12=\'YELLVILLE WATERWORKS\'* 11=S* 35=M* 36=NAD27*',
            'USGS 480042108433301 6=05* 7=05* 8=089* 20=11010003* 802=NNNNNNNNNNNNYNNNNNNN*',
            'USGS 480042108433301 39=WS* 813=CST* 814=Y* 3=C* 41=US*'
        ]

        self.long_line = [
            'USGS 480042108433301 R=0* T=A* 12=\'YELLVILLE WATERWORKS JUNK JUNK JUNK JUNK STUFF STUFF STUFF STUFF\'* 11=S* 35=M* 36=NAD27*',
            'USGS 480042108433301 39=WS* 813=CST* 814=Y* 3=C* 41=US*'
        ]

        self.invalid_site_number_long = [
            'USGS 4800421084333012R=0* T=A* 12=\'YELLVILLE WATERWORKS\'* 11=S* 35=M* 36=NAD27*',
            'USGS 48004210843330116=05* 7=05* 8=089* 20=11010003* 802=NNNNNNNNNNNNYNNNNNNN*',
            'USGS 480042108433301339=WS* 813=CST* 814=Y* 3=C* 41=US*'
        ]

        self.invalid_site_number_short = [
            'USGS 48004210843330 R=0* T=A* 12=\'YELLVILLE WATERWORKS\'* 11=S* 35=M* 36=NAD27*',
            'USGS 48004210843330 6=05* 7=05* 8=089* 20=11010003* 802=NNNNNNNNNNNNYNNNNNNN*',
            'USGS 48004210843331 39=WS* 813=CST* 814=Y* 3=C* 41=US*'
        ]

        self.invalid_site_number_very_short = [
            'USGS 48 R=0*',
            'USGS 48 6=05*',
            'USGS 48 39=WS*'
        ]

        self.multi_errors = [
            'USGS 4800421084333012R=0* T=A* 12=\'YELLVILLE WATERWORKS\'* 11=S* 35=M* 36=NAD27*',
            'USGS 48004210843330 R=0* T=A* 12=\'YELLVILLE WATERWORKS\'* 11=S* 35=M* 36=NAD27*',
            'USGS 480042108433301 39=WS* 813=CST* 814=Y* 3=C* 41=US*',
            'USGS 480042108433301 R=0* T=A* 12=\'YELLVILLE WATERWORKS JUNK JUNK JUNK JUNK STUFF STUFF STUFF STUFF\'* 11=S* 35=M* 36=NAD27*'
        ]

    def test_with_valid_lines(self):
        result = validate_lines(self.location1)
        self.assertEqual(len(result), 0)

    def test_with_line_too_long(self):
        result = validate_lines(self.long_line)
        self.assertEqual(result, "Contains lines exceeding 80 characters: lines 2. ")

    def test_with_invalid_site_number_long(self):
        result = validate_lines(self.invalid_site_number_long)
        self.assertEqual(result, "Contains lines with invalid site number format: lines 2, 3, 4.")

    def test_with_invalid_site_number_short(self):
        result = validate_lines(self.invalid_site_number_short)
        self.assertEqual(result, "Contains lines with invalid site number format: lines 2, 3, 4.")
    
    def test_with_invalid_site_number_very_short(self):
        result = validate_lines(self.invalid_site_number_very_short)
        self.assertEqual(result, "Contains lines with invalid site number format: lines 2, 3, 4.")

    def test_with_multi_error(self):
        result = validate_lines(self.multi_errors)
        self.assertEqual(result, "Contains lines exceeding 80 characters: lines 5. Contains lines with invalid site number format: lines 2, 3.")
    
class ParseTestCase(TestCase):

    def setUp(self):
        self.maxDiff = None

        self.location1_transaction_start = 'USGS 480042108433301 R=0* T=A*'
        self.location1 = (
            'USGS 480042108433301 R=0* T=A* 12=\'YELLVILLE WATERWORKS\'* 11=S* 35=M* 36=NAD27*\r\n'
            'USGS 480042108433301 6=05* 7=05* 8=089* 20=11010003* 802=NNNNNNNNNNNNYNNNNNNN*\r\n'
            'USGS 480042108433301 39=WS* 813=CST* 814=Y* 3=C* 41=US*'
        )
        self.location2 = (
            'USEPA123456789012345 R=0* T=A* 12=\'INTAKE ON LAKE WOBEGON\'* 802=FA-DV\n'
            'USEPA123456789012345 Long Line* 35=* 36=NAD27* 6=05* 7=05* 8=023* 20=11010014*'
        )

        self.location3 = (
            'USGS 580042108433301 R=0* T=A*\n'
            'USGS 580042108433301 12'
        )
        self.non_location = (
            'USGS 680042108433301 R=1* T=A* 12=\'YELLVILLE WATERWORKS\'*'
        )

        self.missing_transaction_type = (
            'USGS 680042108433301 R=1* 12=\'YELLVILLE WATERWORKS\'*'
        )

        self.invalid_component_codes = (
            'USEPA123456789012345 R=0 * T=A * 12=\'INTAKE ON LAKE WOBEGON\'*\r\n'
            'USEPA123456789012345 802=FA-DV* 999=This* 998=That*\n'
        )

        self.long_line = (
            'USGS 480042108433301 R=0* T=A* 12=\'YELLVILLE WATERWORKS JUNK JUNK JUNK JUNK STUFF STUFF STUFF STUFF\'* 11=S* 35=M* 36=NAD27*\n'
            'USGS 480042108433301 39=WS* 813=CST* 814=Y* 3=C* 41=US*'
        )

        self.invalid_site_number_long = (
            'USGS 4800421084333012R=0* T=A* 12=\'YELLVILLE WATERWORKS\'* 11=S* 35=M* 36=NAD27*\r\n'
            'USGS 48004210843330116=05* 7=05* 8=089* 20=11010003* 802=NNNNNNNNNNNNYNNNNNNN*\r\n'
            'USGS 480042108433301339=WS* 813=CST* 814=Y* 3=C* 41=US*'
        )

        self.invalid_site_number_short = (
            'USGS 48004210843330 R=0* T=A* 12=\'YELLVILLE WATERWORKS\'* 11=S* 35=M* 36=NAD27*\r\n'
            'USGS 48004210843330 6=05* 7=05* 8=089* 20=11010003* 802=NNNNNNNNNNNNYNNNNNNN*\r\n'
            'USGS 48004210843331 39=WS* 813=CST* 814=Y* 3=C* 41=US*'
        )

        self.invalid_site_number_very_short = (
            'USGS 48 R=0*\r\n'
            'USGS 48 6=05*\r\n'
            'USGS 48 39=WS*\r\n'
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
        self.assertIn('lines 2', e.exception.message)

    def test_with_invalid_site_number_long(self):
        with self.assertRaises(ParseError) as e:
            parse('XXXXXXX\n' + self.invalid_site_number_long)
        self.assertIn('lines 2, 3, 4', e.exception.message)

    def test_with_invalid_site_number_short(self):
        with self.assertRaises(ParseError) as e:
            parse('XXXXXXX\n' + self.invalid_site_number_short)
        self.assertIn('lines 2, 3, 4', e.exception.message)

    def test_with_invalid_site_number_very_short(self):
        with self.assertRaises(ParseError) as e:
            parse('XXXXXXX\n' + self.invalid_site_number_very_short)
        self.assertIn('lines 2, 3, 4', e.exception.message)
    
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
        result = parse('XXXXXXX\n' + self.location1 + '\r\n' + self.location2)
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
            'coordinateMethodCode': '',
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

    def test_with_site_web_ready_code_of_c(self):
        result = parse('XXXXXX\n' +
                       self.location1_transaction_start +
                       ' 32=C*'
        )
        self.assertEqual(result[0].get('siteWebReadyCode'), 'Y')

    def test_with_site_web_ready_code_of_not_c(self):
        result = parse('XXXXXX\n' +
                       self.location1_transaction_start +
                       ' 32=P*'
        )
        self.assertEqual(result[0].get('siteWebReadyCode'), 'P')

    def test_with_duplicate_adjacent_transactions(self):
        with self.assertRaises(ParseError) as err:
            result = parse('XXXXX\n' + self.location1 + '\n' + self.location1)
        self.assertIn('Duplicate transaction', err.exception.message)

    def test_with_duplicate_non_adjacent_transactions(self):
        with self.assertRaises(ParseError) as err:
            result = parse('XXXXXX\n' + self.location1 + '\n' + self.location2 + '\n' + self.location1)
        self.assertIn('Duplicate transaction', err.exception.message)

    def test_with_nonsite_transactions(self):
        result = parse('XXXXXX\n' + self.location1 + '\n' + self.non_location + '\n' + self.location2)
        self.assertEqual(len(result), 2)
        sites_in_result = [this_result.get('siteNumber') for this_result in result]
        self.assertNotIn('680042108433301', sites_in_result)

    def test_with_missing_transaction_type(self):
        with self.assertRaises(ParseError) as err:
            result = parse('XXXXX\n' + self.location1 + '\n' + self.missing_transaction_type)
        self.assertIn('Missing "T"', err.exception.message)
        self.assertIn('lines [5]', err.exception.message)

    def test_with_bad_component_values(self):
        with self.assertRaises(ParseError) as err:
            result = parse('XXXXX\n' + self.invalid_component_codes)
        self.assertIn('999, 998', err.exception.message)
        self.assertIn('lines [2, 3]', err.exception.message)

    def test_invalid_transaction_type(self):
        with self.assertRaises(ParseError) as err:
            result = parse('XXXXX\n' + 'USGS 480042108433301 R=0* T=B*')
        self.assertIn('Invalid transaction', err.exception.message)
        self.assertIn('lines [2]', err.exception.message)

    def test_with_latitude_without_space(self):
        result = parse('XXXXXX\n' + self.location1_transaction_start + ' 9=400000*')
        self.assertEqual(result[0]['latitude'], ' 400000')

    def test_with_latitude_with_space(self):
        result = parse('XXXXXX\n' + self.location1_transaction_start + ' 9= 400000*')
        self.assertEqual(result[0]['latitude'], ' 400000')

    def test_with_latitude_with_dash(self):
        result = parse('XXXXXX\n' + self.location1_transaction_start + ' 9=-400000*')
        self.assertEqual(result[0]['latitude'], '-400000')

    def test_empty_latitude(self):
        result = parse('XXXXXX\n' + self.location1_transaction_start + ' 9=*')
        self.assertEqual(result[0]['latitude'], '')

    def test_with_longitude_without_space(self):
        result = parse('XXXXXX\n' + self.location1_transaction_start + ' 10=1000000*')
        self.assertEqual(result[0]['longitude'], ' 1000000')

    def test_with_90_longitude_without_zero(self):
        result = parse('XXXXXX\n' + self.location1_transaction_start + ' 10=900000*')
        self.assertEqual(result[0]['longitude'], ' 0900000')

    def test_with_neg_90_longitude_without_zero(self):
        result = parse('XXXXXX\n' + self.location1_transaction_start + ' 10=-900000*')
        self.assertEqual(result[0]['longitude'], '-0900000')

    def test_with_100_longitude_without_zero(self):
        result = parse('XXXXXX\n' + self.location1_transaction_start + ' 10=1000000*')
        self.assertEqual(result[0]['longitude'], ' 1000000')

    def test_with_neg_100_longitude_without_zero(self):
        result = parse('XXXXXX\n' + self.location1_transaction_start + ' 10=-1000000*')
        self.assertEqual(result[0]['longitude'], '-1000000')

    def test_with_90_longitude_with_zero(self):
        result = parse('XXXXXX\n' + self.location1_transaction_start + ' 10=0900000*')
        self.assertEqual(result[0]['longitude'], ' 0900000')

    def test_with_neg_90_longitude_with_zero(self):
        result = parse('XXXXXX\n' + self.location1_transaction_start + ' 10=-0900000*')
        self.assertEqual(result[0]['longitude'], '-0900000')

    def test_with_longitude_with_space(self):
        result = parse('XXXXXX\n' + self.location1_transaction_start + ' 10= 1000000*')
        self.assertEqual(result[0]['longitude'], ' 1000000')

    def test_with_longitude_with_dash(self):
        result = parse('XXXXXX\n' + self.location1_transaction_start + ' 10=-1000000*')
        self.assertEqual(result[0]['longitude'], '-1000000')

    def test_empty_longitude(self):
        result = parse('XXXXXX\n' + self.location1_transaction_start + ' 10=*')
        self.assertEqual(result[0]['longitude'], '')