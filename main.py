from dotenv import load_dotenv
import os
import requests
# access to environment variable
load_dotenv()
# get api token for request to https://openweathermap.org/
api_key = os.environ.get('API_KEY')
# selected data with specific Latitude and Longitude
lat_long = [(51.507351, -0.127758), (53.408371, -2.991573), (40.712776, -74.005974), (41.874316, -87.631724),
            (38.893883, -77.044142), (43.686677, -79.392166), (49.243843, -123.112445), (35.689133, 51.389524),
            (36.470552, 52.348881), (36.545611, 52.684186), (48.136583, 11.572022), (49.461167, 11.071938)]



