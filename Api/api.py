from flask_restx import Api
from .weather_controller import weather
from .disease_controller import disease_controller
from .recommendation import recommendation_controller

api = Api(
    version="1.0",
    title="Cropify api",
    description="The description about the api",
    doc="/api/",
    validate=True
)   

   
api.add_namespace(recommendation_controller)
api.add_namespace(disease_controller)
api.add_namespace(weather)
