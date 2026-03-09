from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv
import logging

# Load env variables

def extract():
    load_dotenv()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    try:

        engine = create_engine(DATABASE_URL)
        query = "SELECT * FROM bronze.formula1_data"
        df = pd.read_sql(query, con=engine)
        logging.info(f"Successfully loaded {len(df)} rows from SQL table into DataFrame")

    except Exception as e:
        logging.error(f"Failed to load data from SQL: {e}")

    return df