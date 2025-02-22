from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename
from Models import QueryModel
from App import db
import requests

from utils import *


crop = Blueprint('crop', __name__)

@crop.route('/fertilizer', methods = ['GET', 'POST'])
def fertilizer():
    crops = crop_types()
    soils = soil_types()

    if request.method == 'POST':
        n = request.form.get('nitrogen')
        p = request.form.get('phosphorous')
        k = request.form.get('potassium')
        temp = request.form.get('temp')
        hum = request.form.get('humidity')
        mos = request.form.get('Moisture')
        crop = request.form.get('crop')
        soil = request.form.get('soil')

        result = predict_fertilizer(temp, hum, mos, soil, crop, n, p, k)

        context = {
            'crops' : enumerate(crops),
            'soils' : enumerate(soils),
            'result' : result
        }

        return render_template("crop/fertilizer.html", **context)

    context = {
        'crops' : enumerate(crops),
        'soils' : enumerate(soils)
    }

    return render_template("crop/fertilizer.html", **context)


@crop.route('/crop', methods = ['GET', 'POST'])
def crop_recommendation():
    crops = crop_types()
    soils = soil_types()

    if request.method == 'POST':
        n = request.form.get('nitrogen')
        p = request.form.get('phosphorous')
        k = request.form.get('potassium')
        temp = request.form.get('temp')
        hum = request.form.get('humidity')
        rain = request.form.get('Moisture')
        ph = request.form.get('ph')
        soil = request.form.get('soil')

        result = predict_crop(n,p,k,temp,hum,ph, rain)

        context = {
            'crops' : enumerate(crops),
            'soils' : enumerate(soils),
            'result' : result
        }

        return render_template("crop/crop.html", **context)

    context = {
        'crops' : enumerate(crops),
        'soils' : enumerate(soils)
    }

    return render_template("crop/crop.html", **context)
    

@crop.route('/crop-disease')
def crop_disease():
    return render_template("crop/crop-disease.html")

@crop.route('/weather', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        city_name = request.form.get('city_name')

        result = get_weather(city_name)

        return render_template('crop/weather.html', result = result)
    
    return render_template("crop/weather.html")

@crop.route('/former-queries', methods=['GET', 'POST'])
def former_queries():
    if request.method == 'POST':
        title = request.form.get("title")
        file = request.files.get("file")

        filename = 'static/images/queries'+secure_filename(file.filename)
        file.save(filename)

        query = QueryModel(text=title, img_url=filename, userId=session['id'])

        db.session.add(query)
        db.session.commit()

        flash("Query raised successfully", "success")
        return redirect(url_for("crop.former_queries"))

    return render_template('crop/query.html')

def get_weather(city):
    API_KEY = '3MUNGGH2VYWHHDXSBBDN24WHL'
    url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{}/today?unitGroup=metric&include=days&key={}&contentType=json"
    WEATHER_URL = url.format(city, API_KEY)

    response = requests.get(WEATHER_URL)
    if response.status_code == 200:
        result = response.json()
        for res in result['days']:

            if res['icon'] == 'clear-day':
                res['icon_url'] = 'https://www.visualcrossing.com/img/clear-day.c5680783.svg'

            if res['icon'] == 'partly-cloudy-day':
                res['icon_url'] = 'https://www.visualcrossing.com/img/partly-cloudy-day.3f13edae.svg'

            if res['icon'] == 'cloudy':
                res['icon_url'] = 'https://www.visualcrossing.com/img/cloudy.61f1f7c3.svg'

            if res['icon'] == 'rain':
                res['icon_url'] = 'https://www.visualcrossing.com/img/rain.36d72e24.svg'

            if res['icon'] == 'showers-day':
                res['icon_url'] = 'https://www.visualcrossing.com/img/showers-day.2f888a31.svg '

            if res['icon'] == 'showers-night':
                res['icon_url'] = 'https://www.visualcrossing.com/img/showers-night.b7f6058d.svg'

            if res['icon'] == 'thunder-showers-day':
                res['icon_url'] = 'https://www.visualcrossing.com/img/thunder-showers-day.90053223.svg'

            if res['icon'] == 'thunder-rain':
                res['icon_url'] = 'https://www.visualcrossing.com/img/thunder-rain.c575e6f7.svg'

        return result

