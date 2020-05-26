from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import DataBaseConfig


engine = create_engine(DataBaseConfig.url, echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

