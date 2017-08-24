from flask import request
from flask_restplus import Api, Resource
from werkzeug.utils import secure_filename

from app import application

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
        return {
            'message': 'File Uploaded successfully',
            'contents': file_contents.decode()
        }
