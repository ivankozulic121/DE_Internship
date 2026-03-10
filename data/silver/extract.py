from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import logging
from data.db import get_database_url

# Load env variables

def extract():
    load_dotenv()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

    DATABASE_URL = get_database_url()

    try:

        engine = create_engine(DATABASE_URL)
        query = "SELECT * FROM bronze.formula1_staging"
        df = pd.read_sql(query, con=engine)
        logging.info(f"Successfully loaded {len(df)} rows from SQL table into DataFrame")
        

    except Exception as e:
        logging.error(f"Failed to load data from SQL: {e}")

    return df

    