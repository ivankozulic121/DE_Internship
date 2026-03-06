from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
import logging
import os

load_dotenv()

logging.basicConfig(
    level=logging.INFO,   # minimum level to show
    format="%(asctime)s [%(levelname)s] %(message)s"
)


csv_path = os.getenv("DATA_CSV_PATH")

formulaDF = pd.read_csv(csv_path, index_col=0)

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


try:

    engine = create_engine(DATABASE_URL)
    
    formulaDF.to_sql(name='formula1_data', con=engine, schema='bronze', if_exists='append', index=False)
    logging.info("Data successfully loaded to staging table")


except Exception as e:
    logging.error(f"Failed to load data into staging table: {e}")
