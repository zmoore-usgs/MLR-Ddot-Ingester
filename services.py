
import pkg_resources

from flask_restplus import Api, Resource, reqparse, fields
from werkzeug.datastructures import FileStorage

from app import application
from ddot_utils import ParseError, parse as parse_ddot

api = Api(application,
          title='D dot File Ingestor',
          description='Provides a service to upload a "d." file, parse it, and respond back with a response containing the parsed information',
          default='Ddot ingestor',
          default_label='Ddot Ingestor Endpoint',
          doc='/api')

location_transaction_model = api.model('LocationTransactionModel', {
    'agencyCode': fields.String(),
    'siteNumber': fields.String(),
    'stationName': fields.String(),
    'siteTypeCode': fields.String(),
    'latitude': fields.String(),
    'longitude': fields.String(),
    'coordinateAccuracyCode': fields.String(),
    'coordinateDatumCode': fields.String(),
    'coordinateMethodCode': fields.String(),
    'altitude': fields.String(),
    'altitudeDatumCode': fields.String(),
    'altitudeMethodCode': fields.String(),
    'altitudeAccuracyValue': fields.String(),
    'districtCode': fields.String(),
    'countryCode': fields.String(),
    'stateFipsCode': fields.String(),
    'countyCode': fields.String(),
    'minorCivilDivisionCode': fields.String(),
    'hydrologicUnitCode': fields.String(),
    'basinCode': fields.String(),
    'nationalAquiferCode': fields.String(),
    'aquiferCode': fields.String(),
    'aquiferTypeCode': fields.String(),
    'agencyUseCode': fields.String(),
    'dataReliabilityCode': fields.String(),
    'landNet': fields.String(),
    'mapName': fields.String(),
    'mapScale': fields.String(),
    'nationalWaterUseCode': fields.String(),
    'primaryUseOfSite': fields.String(),
    'secondaryUseOfSite': fields.String(),
    'tertiaryUseOfSiteCode': fields.String(),
    'primaryUseOfWaterCode': fields.String(),
    'secondaryUseOfWaterCode': fields.String(),
    'tertiaryUseOfWaterCode': fields.String(),
    'topographicCode': fields.String(),
    'dataTypesCode': fields.String(),
    'instrumentsCode': fields.String(),
    'contributingDrainageArea': fields.String(),
    'drainageArea': fields.String(),
    'firstConstructionDate': fields.String(),
    'siteEstablishmentDate': fields.String(),
    'holeDepth': fields.String(),
    'wellDepth': fields.String(),
    'sourceOfDepthCode': fields.String(),
    'projectNumber': fields.String(),
    'timeZoneCode': fields.String(),
    'daylightSavingsTimeFlag': fields.String(),
    'remarks': fields.String(),
    'siteWebReadyCode': fields.String(),
    'gwFileCode': fields.String(),
    'databaseTableIdentifier': fields.String(),
    'transactionType': fields.String(),
})
error_model = api.model('ErrorModel', {
    'error_message': fields.String(required=True)
})

parser = reqparse.RequestParser()
parser.add_argument('file', type=FileStorage, location='files', required=True)


@api.route('/ddots')
class DdotIngester(Resource):

    @api.response(200, 'Successfully uploaded and parsed', [location_transaction_model])
    @api.response(400, 'File can not be parsed', error_model)
    @api.expect(parser)
    def post(self):
        args = parser.parse_args()
        f = args['file']
        file_contents = f.read()
        try:
            result = parse_ddot(file_contents.decode())
        except ParseError as err:
            response, status = {
                'error_message': err.message
            }, 400
        else:
            response, status = result, 200

        return response, status


version_model = api.model('VersionModel', {
    'version': fields.String,
    'artifact': fields.String
})


@api.route('/version')
class Version(Resource):

    @api.response(200, 'Success', version_model)
    def get(self):
        try:
            distribution = pkg_resources.get_distribution('usgs_wma_mlr_ddot_ingester')
        except pkg_resources.DistributionNotFound:
            resp = {
                "version": "local_development",
                "artifact": None
            }
        else:
            resp = {
                "version": distribution.version,
                "artifact": distribution.project_name
            }
        return resp
