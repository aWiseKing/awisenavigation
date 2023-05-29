from sqlalchemy import create_engine,Column, ForeignKey, Integer, String, DateTime,text
from sqlalchemy.ext.declarative import declarative_base
from config import configs
from sqlalchemy.orm import sessionmaker
Base = declarative_base()
engine = create_engine(configs["default"].SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)

