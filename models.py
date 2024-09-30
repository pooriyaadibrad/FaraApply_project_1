# import module
from sqlalchemy import create_engine, Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import declarative_base, Relationship
from dotenv import load_dotenv
import os

# for load environment variable
load_dotenv()
"""base setting for connect to postgres with sqlalchemy"""
# connection string
engine = create_engine(os.environ.get("DATABASE_URL"))
# base model for inherite to my models
Base = declarative_base()

"""my model for designing DataBase"""
class City(Base):
    """City model for stored cities data"""
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    city_name = Column(String)
    country = Column(String)
    coord_lat = Column(Float)
    coord_lon = Column(Float)
    Weather = Relationship('Weather',back_populates='City')
    def __repr__(self):
        return f'{self.city_name} - {self.country} '


class Weather(Base):
    """Weather model for stored weather data"""
    __tablename__ = 'weather'
    # attribute
    id = Column(Integer, primary_key=True)
    date = Column(String)
    time = Column(String)
    temperature = Column(Float)
    humidity = Column(Float)
    wind_speed = Column(Float)
    # association
    City = Relationship('City', back_populates='Weather')
    city_id = Column(Integer, ForeignKey('city.id'))

    def __repr__(self):
        return f'{self.time} - {self.temperature} - {self.humidity} - {self.wind_speed}'

"""Table Builder"""
Base.metadata.create_all(engine)
