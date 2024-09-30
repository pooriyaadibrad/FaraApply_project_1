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

    def __repr__(self):
        return f'{self.city_name} - {self.country} '


"""Table Builder"""
Base.metadata.create_all(engine)
