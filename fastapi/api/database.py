from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

<<<<<<< HEAD
SQL_ALCHEMY_DATABASE_URL = 'sqlite:///workout_app.db'
=======
SQL_ALCHEMY_DATABASE_URL = 'sqlite:///rental_car_app.db'
>>>>>>> 06f716055b3c6dd1cc385fbd15a6aa910770b7e9

engine = create_engine(SQL_ALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()