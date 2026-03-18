from .transform import transform
from .extract import extract
from sqlalchemy import text
from dotenv import load_dotenv
import logging
import pandas as pd
from io import StringIO
from data.db import engine

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def load():
    dataFrame = transform()
    try:

        with engine.begin() as conn:  
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS silver"))

            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS silver.formula1_silver
                (LIKE bronze.formula1_staging INCLUDING ALL)
            """))

            conn.execute(text("TRUNCATE TABLE silver.formula1_silver"))

            logging.info("Table ready for load")
            logging.info(f"Schema silver exists and table truncated/created")

            buffer = StringIO()
            dataFrame.to_csv(buffer, index=False, header=False, na_rep='\\N')  # \N = NULL in PostgreSQL
            buffer.seek(0)
            
            chunksize = 100000
            columns = ', '.join([f'"{col}"' for col in dataFrame.columns])

            cursor = conn.connection.cursor()
            for start in range(0, len(dataFrame), chunksize):
                buffer = StringIO()
                dataFrame.iloc[start:start+chunksize].to_csv(buffer, index=False, header=False, na_rep='\\N')
                buffer.seek(0)
                cursor.copy_expert(
                    f"COPY silver.formula1_silver ({columns}) FROM STDIN WITH CSV NULL '\\N'",
                    buffer
                )

        logging.info(f"DataFrame successfully loaded into silver.formula1_silver")

    except Exception as e:
        logging.error(f"Failed to upload DataFrame to SQL: {e}")
        raise  # Propagate error

if __name__ == "__main__":
    load()