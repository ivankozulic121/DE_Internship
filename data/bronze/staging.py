from sqlalchemy import text
from .models.models import Base
from dotenv import load_dotenv
import logging
from data.db import engine

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def create_bronze_table():
    try:
        with engine.begin() as conn:
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS bronze"))
            conn.commit()

        Base.metadata.create_all(engine)

        logging.info("Bronze schema table successfully created.")

    except Exception as e:
        logging.error(f"Failed to create tables: {e}")


if __name__ == "__main__":
    create_bronze_table()