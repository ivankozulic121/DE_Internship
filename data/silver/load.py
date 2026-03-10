from .transform import transform
from .extract import extract
from sqlalchemy import create_engine
from dotenv import load_dotenv
import logging
import pandas as pd
from data.db import get_database_url


load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def load(DATABASE_URL, dataFrame):
    try:
        engine = create_engine(DATABASE_URL)

        schema='silver'
        table_name = 'formula1_silver'

        dataFrame.to_sql(name=table_name,con=engine, schema=schema, index=False, if_exists='replace')
        
        logging.info(f"DataFrame successfully loaded into {schema}.{table_name}")

    except Exception as e:
        logging.error(f"Failed to upload DataFrame to SQL: {e}")



if __name__ == "__main__":
    DATABASE_URL = get_database_url()
    df = extract(DATABASE_URL)
    df_transformed = transform(df)
    load(DATABASE_URL, df_transformed)
