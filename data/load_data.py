from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from clean_data import formulaDF
import logging
import os
from models.models import Base

load_dotenv()

logging.basicConfig(
    level=logging.INFO,   # minimum level to show
    format="%(asctime)s [%(levelname)s] %(message)s"
)

DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "secret_password")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "mydatabase")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"



def load_data_to_db():
    try:
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        session = Session()
        Base.metadata.create_all(engine)
        logging.info("Models successfully created in the database.")

    except Exception as e:
        logging.error(f"Failed to upload models to database: {e}")

load_data_to_db()