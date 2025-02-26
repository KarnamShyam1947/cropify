from flask_restx import Namespace, Resource, reqparse
from werkzeug.datastructures import FileStorage
from Api.predict import classify_using_bytes
from .solution import solution

disease_controller = Namespace(
    "disease-api",
    "get diseases details here",
    "/disease-api"
)

photoReqParse=reqparse.RequestParser()
photoReqParse.add_argument('images', location='files', type=FileStorage)

@disease_controller.route('/disease-prediction')
class DiseaseController(Resource):   
    
    @disease_controller.expect(photoReqParse)
    def post(self):
        args = photoReqParse.parse_args()
        file = args['images']

        if file:
            raw_result = classify_using_bytes(file.read(), 'Api/models/model.h5', 224)
            print(f'raw result {raw_result}')
            result = solution.get(raw_result['idx'] + 1)
            result['score'] = raw_result['score']
            return result

        else:
            print("\n404 no file found\n")
 