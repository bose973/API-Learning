from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

# Database connection format that we have to provide to sqlalchemy for making the db connection
# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
# engine=create_engine(SQLALCHEMY_DATABASE_URL) #to establish the connection

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
engine=create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#RealDictCursor is used to fetch the column name as well
# while True:
#         try:
#                 conn=psycopg2.connect(host='localhost',database='learnAPI',user='postgres',
#                 password='sid123', cursor_factory=RealDictCursor)
#                 cursor=conn.cursor()
#                 print("DataBase connection was successful!")
#                 break
#         except Exception as error:
#                 print("Connecting failed")
#                 print(f"Error was {error}")
#                 time.sleep(3)

# def findPost(id):
#         cursor.execute("""SELECT * FROM posts WHERE id=%s; """,(str(id)))
#         post=cursor.fetchone()
#         return post