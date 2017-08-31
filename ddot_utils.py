import itertools
import re

KEY_TO_ATTR_MAPPING = {
    '61': 'createBy',
    '303': 'created',
    '62': 'updatedBy',
    '40': 'updated',
    '5': 'projectNumber',
    '900': 'stationName',
    '12': 'stationName',
    '802': 'siteTypeCode',
    '6': 'districtCode',
    '41': 'countryCode',
    '7': 'stateFipsCode',
    '8': 'countyCode',
    '42': 'minorCivilDivisionCode',
    '9': 'latitude',
    '10': 'longitude',
    '909': 'decimalLatitude',
    '910': 'decimalLongitude',
    '11': 'coordinateAccuracyCode',
    '35': 'coordinateMethodCode',
    '36': 'coordinateDatumCode',
    '16': 'altitude',
    '18': 'altitudeAccuracyValue',
    '17': 'altitudeMethodCode',
    '22': 'altitudeDatumCode',
    '13': 'landNet',
    '19': 'topographicCode',
    '20': 'hydrologicUnitCode',
    '801': 'basinCode',
    '813': 'timeZoneCode',
    '814': 'daylightSavingsTimeFlag',
    '14': 'mapName',
    '15': 'mapScale',
    '803': 'agencyUseCode',
    '39': 'nationalWaterUseCode',
    '804': 'dataTypesCode',
    '805': 'instrumentsCode',
    '711': 'siteEstablishmentDate',
    '806': 'remarks',
    '32': 'siteWebReadyCode',
    '3': 'dataReliabilityCode',
    '21': 'firstConstructionDate',
    '23': 'primaryUseOfSiteCode',
    '301': 'secondaryUseOfSiteCode',
    '302': 'tertiaryUseOfSiteCode',
    '24': 'primaryUseOfWaterCode',
    '25': 'secondaryUseOfWaterCode',
    '26': 'tertiaryUseOfWaterCode',
    '713': 'aquiferTypeCode',
    '714': 'aquiferCode',
    '715': 'nationalAquiferCode',
    '27': 'holeDepth',
    '28': 'wellDepth',
    '29': 'sourceOfDepthCode',
    '808': 'drainageArea',
    '809': 'contributingDrainageArea',
    '712': 'gwFileCode',
    'R': 'databaseTableIdentifier',
    'T': 'transactionType'
}

class ParseError(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'ParseError, message: {0}'.format(self.message)


def get_lines(content):
    '''

    :param str content:
    :rtype: list of str
    :return: List of lines within content that contain ddot data
    :raises ParseError if any of the lines exceeds 80 characters
    '''
    if not content:
        raise ParseError('No contents found')
    lines = content.split('\n')[1:]

    if not lines:
        raise ParseError('No transactions found')

    # Remove trailing line feed
    if not lines[len(lines) - 1]:
        lines = lines[0:len(lines) - 1]

    lines_with_errors = []
    for index, line in enumerate(lines):
        if len(line) > 80:
            lines_with_errors.append(index + 2)

    if lines_with_errors:
        raise ParseError('Contains lines exceeding 80 characters: line {0}'.format(', '.join([str(line) for line in lines_with_errors])))

    return lines



def get_transactions(lines):
    '''

    :param list of str lines:
    :rtype: list of dicts for each location in content
    :return: Returns a list of dictionaries. Each dictionary has three properties:
        agencyCode contains a string agency code, siteNumber contains the string site number,
        and 'key_value_pairs' returns all of the key value pairs concatenated for the location
    '''

    # line indexes are incremented by two to account for the intro line and that the array starts at zero
    parsed_lines = [(line[0:20], line[21:], index + 2) for index, line in enumerate(lines)]
    result = []

    for location, location_group in itertools.groupby(parsed_lines, lambda x: x[0]):
        line_numbers = []
        key_value_pairs = []
        for line in location_group:
            key_value_pairs.append(line[1])
            line_numbers.append(line[2])
        transaction = {
            'agencyCode' : location[0:5],
            'siteNumber': location[5:20],
            'key_value_pairs': ' '.join(key_value_pairs),
            'line_numbers': line_numbers
        }
        result.append(transaction)

    return result


def parse_key_value_pairs(kv_pairs_str):
    '''
    :param kv_pairs_str:
    :return:list of tuples with the form [(d.Code, value)...]
    :raises ParseError if the string does not contain valid key value pairs. Possible errors
        include not finding a separator token or not finding an ending token
    '''

    SEPARATOR_TOKENS = re.compile('[=#]')
    VALUE_ENDING_TOKENS = re.compile('[\*\$]')

    test_string = kv_pairs_str
    result = []
    if not kv_pairs_str:
        raise ParseError('No key value pairs found')

    while (test_string):
        separator_match = SEPARATOR_TOKENS.search(test_string)
        if not separator_match:
            raise ParseError('Incomplete key value pair with no separator in {0}'.format(test_string))

        key = test_string[0:separator_match.start()]
        value_ending_match = VALUE_ENDING_TOKENS.search(test_string)
        if value_ending_match:
            value = test_string[separator_match.end():value_ending_match.start()]
        else:
            raise ParseError('Could not find value ending token in {0}'.format(test_string))
        result.append((key, value))

        test_string = test_string[value_ending_match.end() + 1:]

    return result


def has_duplicate_station_name_keys(kv_pairs):
    '''
    :param list of tuples kv_pairs:
    :return: list of dicts

    '''
    found = False
    has_duplicate = False
    for (key, value) in kv_pairs:
        if KEY_TO_ATTR_MAPPING.get(key) == 'stationName':
            if found:
                has_duplicate = True
                break
            else:
                found = True
    return has_duplicate


def translate_keys_to_attributes(kv_pairs):
    '''
    :param list of tuples kv_pairs:
    :return: dict
    '''
    result = {KEY_TO_ATTR_MAPPING.get(key): value for (key, value) in kv_pairs if key in KEY_TO_ATTR_MAPPING}
    return result


def parse(file_contents):
    '''

    :param file_contents:
    :return: array of dictionary. Each dictionary contains a transaction for a site parsed from file_contents
    :raises: ParseError with an appropriate message if unable to parse file.
    '''

    lines = get_lines(file_contents)
    transactions = get_transactions(lines)
    result = []
    for transaction in transactions:
        this_result = {
            'agencyCode': transaction.get('agencyCode'),
            'siteNumber': transaction.get('siteNumber')
        }
        try:
            kv_pairs = parse_key_value_pairs(transaction.get('key_value_pairs'))
        except ParseError as err:
            raise ParseError('Parsing error on lines{0}: line {1}'.format(transaction.get('line_numbers'), err.message))

        if has_duplicate_station_name_keys(kv_pairs):
            raise ParseError('Parsing error on lines {0}: Duplicate station name codes'.format(transaction.get('line_numbers')))

        this_result = translate_keys_to_attributes(kv_pairs)
        this_result['agencyCode'] = transaction.get('agencyCode')
        this_result['siteNumber'] = transaction.get('siteNumber')
        result.append(this_result)

    return result















