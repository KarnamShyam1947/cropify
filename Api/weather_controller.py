from flask_restx import Resource, Namespace, abort
from flask import request
import requests

weather = Namespace('Weather Api', path='/weather-api')

API_KEY = '3MUNGGH2VYWHHDXSBBDN24WHL'

@weather.route('/current/<string:city>')
class CurrentWeatherResource(Resource):
    def get(self, city):
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

        else:
            abort(404, status='failed', message="SORRY! Unable to find the city")


@weather.route('/forecast/<string:city>')
class ForecastWeatherResource(Resource):
    def get(self, city):
        BASE_URL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{}?unitGroup=metric&include=days&key={}&contentType=json'
        WEATHER_URL = BASE_URL.format(city, API_KEY)

        response = requests.get(WEATHER_URL)
        result = response.json()

        days = request.args.get('days')
        if days:
            days = int(days)
            result['days'] = result['days'][0:days]

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

