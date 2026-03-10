from sqlalchemy import create_engine, text
from .models.models import Base
from dotenv import load_dotenv
import logging
from data.db import get_database_url

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

DATABASE_URL = get_database_url()

def create_bronze_tables():
    try:
        engine = create_engine(DATABASE_URL)

        with engine.connect() as conn:
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS bronze"))
            conn.commit()

        Base.metadata.create_all(engine)

        logging.info("Bronze schema table successfully created.")

    except Exception as e:
        logging.error(f"Failed to create tables: {e}")


if __name__ == "__main__":
    create_bronze_tables()