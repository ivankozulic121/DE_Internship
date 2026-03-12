import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
import logging
import os
from data.db import engine

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def load_bronze_table():
    try:
        csv_path = os.getenv("DATA_CSV_PATH")
        if not csv_path:
            raise ValueError("DATA_CSV_PATH not set in environment variables")
        
        df = pd.read_csv(csv_path)

        df.to_sql(
            name='formula1_staging',
            con=engine,
            schema='bronze',
            if_exists='replace',
            index=False
        )
        logging.info("Data successfully loaded to staging table")

    except Exception as e:
        logging.error(f"Failed to load data into staging table: {e}")
        raise

if __name__ == "__main__":
    load_bronze_table()