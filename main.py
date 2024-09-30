from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import requests
import models

# access to environment variable
load_dotenv()
# get api token for request to https://openweathermap.org/
api_key = os.environ.get('API_KEY')
# selected data with specific Latitude and Longitude
lat_long = [(51.507351, -0.127758), (53.408371, -2.991573), (40.712776, -74.005974), (41.874316, -87.631724),
            (38.893883, -77.044142), (43.686677, -79.392166), (49.243843, -123.112445), (35.689133, 51.389524),
            (36.470552, 52.348881), (36.545611, 52.684186), (48.136583, 11.572022), (49.461167, 11.071938)]


def request_api(lat_long_var):
    """
    a tuple that carries Latitude and Longitude:param lat_long_var:tuple
    a json that carries all data like weather , city , etc.:return: json
    """
    return requests.get(
        f'https://api.openweathermap.org/data/2.5/forecast?lat={lat_long_var[0]}&lon={lat_long_var[1]}&appid={api_key}')


def register_weather_data(data):
    """
    this function registers weather data and city data
    in database and Builds a relationship with city and weather

    all data we are getting from open weather site:param data:json
    None:return:None
    """
    city = models.City(id=data['city']['id'], city_name=data['city']['name'],
                       country=data['city']['country'],
                       coord_lat=data['city']['coord']['lat'], coord_lon=data['city']['coord']['lon'])
    """register data in data base"""
    session.add(city)
    session.commit()

    for forecast in data['list']:
        weather = models.Weather(date=forecast['dt_txt'][0:10], time=forecast['dt_txt'][11:19],
                                 temperature=forecast['main']['temp'],
                                 humidity=forecast['main']['humidity'],
                                 wind_speed=forecast['wind']['speed'], city_id=city.id)
        """register data in data base"""
        session.add(weather)
        session.commit()
    """close connection"""
    session.close()


"""connection to data base"""
engine = create_engine(os.environ.get("DATABASE_URL"))
"""interaction with database"""
Session = sessionmaker(bind=engine)
session = Session()

