from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker ,declarative_base, Session


DB_URL = "mysql+pymysql://root:root@localhost:3306/streaming"

engine= create_engine(DB_URL)
session = sessionmaker(autoflush=False, bind=engine)

Base=declarative_base()