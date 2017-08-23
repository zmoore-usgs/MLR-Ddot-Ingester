from flask_restplus import Api, Resource

from app import application

api = Api(application,
          title='D dot File Ingestor',
          description='Provides a service to upload a "d." file, parse it, and respond back with a response containing the parsed information',
          default='Ddot ingestor',
          default_label='Ddot Ingestor Endpoint',
          doc='/api')

@api.route('/ddots')
class DdotIngester(Resource):

    def post(self):
        return 'Not yet implemented'