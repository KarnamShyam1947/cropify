import pandas as pd
import pickle as plk

fertilizer_data = pd.read_csv('data/Fertilizer_Prediction.csv')

def soil_types():
    soil_type = fertilizer_data['Soil Type'].unique().tolist()
    soil_type.sort()
    
    return soil_type

def crop_types():
    crop_type = fertilizer_data['Crop Type'].unique().tolist()
    crop_type.sort()

    return crop_type

def predict_fertilizer(temp, hum, mos, soil, crop, n, p, k):
    with open('models/fertilizer.pkl', 'rb') as f:
        model = plk.load(f)

    input_data = [temp, hum, mos, soil, crop, n, p, k]
    result = model.predict([input_data])

    return result[0]

def predict_crop(N,P,K,temperature,humidity,ph,rainfall):
    input_data = [N, P, K, temperature, humidity, ph, rainfall]

    with open('models/crop.pkl', 'rb') as f:
        model = plk.load(f)

    result = model.predict([input_data])

    return result[0]
