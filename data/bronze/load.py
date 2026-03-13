import psycopg2
from dotenv import load_dotenv
from sqlalchemy import text
import logging
import os
import io
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
        
        with engine.begin() as conn:
            conn.execute(text("TRUNCATE TABLE bronze.formula1_staging"))
            
            # Koristi COPY za najbrže učitavanje
            with open(csv_path, 'r', encoding='utf-8') as f:
                # Preskoči header ako postoji
                
                # PostgreSQL COPY komanda
                cursor = conn.connection.cursor()
                cursor.copy_expert(
                    """
                    COPY bronze.formula1_staging 
                    FROM STDIN WITH (
                    FORMAT CSV,
                    HEADER TRUE,
                    DELIMITER ',',
                    QUOTE '"'
                    """, 
                    f
                )
            
            logging.info("Data successfully loaded to staging table using COPY")

    except Exception as e:
        logging.error(f"Failed to load data into staging table: {e}")
        raise

if __name__ == "__main__":
    load_bronze_table()