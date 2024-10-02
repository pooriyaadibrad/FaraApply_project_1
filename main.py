from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import requests
import models
import pandas as pd
import datetime
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
    message:return:string
    """
    city = models.City(id=data['city']['id'], city_name=data['city']['name'],
                       country=data['city']['country'],
                       coord_lat=data['city']['coord']['lat'], coord_lon=data['city']['coord']['lon'])
    """register data in data base"""
    condition = session.query(models.City).filter_by(id=data['city']['id']).first()
    if not condition:
        session.add(city)
        session.commit()
    else:
        return 'this data be Register in past'

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
    return 'data registered successfully'


"""connection to data base"""
engine = create_engine(os.environ.get("DATABASE_URL"))
"""interaction with database"""
Session = sessionmaker(bind=engine)
session = Session()

if __name__ == '__main__':
    for lat_long_step in lat_long:
        while True:
            response = request_api(lat_long_step)
            if response.status_code == 200:
                result = response.json()
                print(register_weather_data(result))
                break
    print('Done fetching data')

    """list of all cities in data frame"""
    # fetching cities data from data base
    cities = session.query(models.City).all()
    df = pd.DataFrame({
                          'city_name': city.city_name,
                          'country': city.country,
                          'coord_lat': city.coord_lat,
                          'coord_lon': city.coord_lon,
                      } for city in cities
                      )
    print(df)
    """list of all weather information in data frame"""
    # fetching cities data from data base
    weather_info = session.query(models.Weather).all()
    all_weather_every_city=[]
    for city in cities:
        df_1 = pd.DataFrame({
                                'date': w.date,
                                'time': w.time,
                                'temperature': w.temperature,
                                'humidity': w.humidity,
                                'wind_speed': w.wind_speed,
                                'city_name': city.city_name
                            } for w in weather_info
                            )
        """ 
        with this query we can define want 24h data of every city
        select_24h is only int data 
        """
        try:
            select_24h = session.query(models.Weather).filter_by(date=str(datetime.date.today())).filter_by(
                city_id=session.query(models.City).all()[0].id).all()
        except ValueError:
            print('in register city we have problem')
            select_24h=0

        print(df_1.head(len(select_24h)+1))
        # with this code caching every cities data that fetching from database
        all_weather_every_city.append(df_1)
    """represent to us all weather information in database for every city"""
    for w_1 in all_weather_every_city:
        print(w_1)
