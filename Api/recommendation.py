from flask_restx import Namespace, Resource, reqparse
import pickle as plk

recommendation_controller=Namespace(
    "recommendation-api",
    path="/recommendation-api"
)

cropArgs = reqparse.RequestParser()
cropArgs.add_argument('n', location='form', type=int)
cropArgs.add_argument('p', location='form', type=int)
cropArgs.add_argument('k', location='form', type=int)
cropArgs.add_argument('ph', location='form', type=int)
cropArgs.add_argument('hum', location='form', type=int)
cropArgs.add_argument('temp', location='form', type=int)
cropArgs.add_argument('rain', location='form', type=int)

fetArgs = reqparse.RequestParser()
fetArgs.add_argument('n', location='form', type=int)
fetArgs.add_argument('p', location='form', type=int)
fetArgs.add_argument('k', location='form', type=int)
fetArgs.add_argument('hum', location='form', type=int)
fetArgs.add_argument('mos', location='form', type=int)
fetArgs.add_argument('soil', location='form', type=int)
fetArgs.add_argument('crop', location='form', type=int)
fetArgs.add_argument('temp', location='form', type=int)

@recommendation_controller.route("/crop")
class CropRecommendation(Resource):
    
    @recommendation_controller.expect(cropArgs)
    def post(self):
        args = cropArgs.parse_args()
        print(args)

        n = args.get('n')
        p = args.get('p')
        k = args.get('k')
        ph = args.get('ph')
        hum = args.get('hum')
        temp = args.get('temp')
        rain = args.get('rain')


        result = predict_crop(n,p,k,temp,hum,ph,rain)

        return result

@recommendation_controller.route("/fertilizer")
class FertilizerRecommendation(Resource):
    
    @recommendation_controller.expect(fetArgs)
    def post(self):
        args = fetArgs.parse_args()

        n = args.get('n')
        p = args.get('p')
        k = args.get('k')
        hum = args.get('hum')
        mos = args.get('mos')
        soil = args.get('soil')
        temp = args.get('temp')
        crop = args.get('crop')

        result = predict_fertilizer(temp, hum, mos, soil, crop, n, p, k)

        return result

def predict_fertilizer(temp, hum, mos, soil, crop, n, p, k):
    with open('Api/models/fertilizer.pkl', 'rb') as f:
        model = plk.load(f)

    input_data = [temp, hum, mos, soil, crop, n, p, k]
    result = model.predict([input_data])

    return result[0]

def predict_crop(N,P,K,temperature,humidity,ph,rainfall):
    input_data = [N, P, K, temperature, humidity, ph, rainfall]

    with open('Api/models/crop.pkl', 'rb') as f:
        model = plk.load(f)

    result = model.predict([input_data])

    return result[0]
