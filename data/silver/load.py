from transform import transform
from sqlalchemy import create_engine
from dotenv import load_dotenv
import logging
import pandas as pd
import os


formulaDF = transform()


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

    schema='silver'
    table_name = 'formula1_silver'

    formulaDF.to_sql(name=table_name,con=engine, schema=schema, index=False, if_exists='replace')
    
    logging.info(f"DataFrame successfully loaded into {schema}.{table_name}")

except Exception as e:
    logging.error(f"Failed to upload DataFrame to SQL: {e}")