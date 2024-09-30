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

"""Table Builder"""
Base.metadata.create_all(engine)
