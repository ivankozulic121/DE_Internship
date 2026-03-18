import logging
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from .models.models import Base
from data.db import engine

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def load_models():
    try:
        with engine.begin() as conn:  
            conn.execute(text("DROP SCHEMA IF EXISTS gold CASCADE"))
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS gold"))

            Base.metadata.create_all(bind=conn)
            logging.info("All tables successfully loaded into gold schema.")

    except Exception as e:
        logging.error(f"Error loading tables into DB: {e}")


if __name__ == "__main__":
    load_models()
