from flask import request
from flask_restplus import Api, Resource


from app import application
from ddot_utils import ParseError, parse as parse_ddot

api = Api(application,
          title='D dot File Ingestor',
          description='Provides a service to upload a "d." file, parse it, and respond back with a response containing the parsed information',
          default='Ddot ingestor',
          default_label='Ddot Ingestor Endpoint',
          doc='/api')

@api.route('/ddots')
class DdotIngester(Resource):

    @api.param('file','file')
    def post(self):
        f = request.files['file']
        file_contents = f.read()
        try:
            result = parse_ddot(file_contents.decode())
        except ParseError as err:
            response, status = {
                'message': err.message
            }, 400
        else:
            response, status = result, 200

        return response, status
