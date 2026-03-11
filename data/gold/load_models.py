import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models.models import Base
from data.db import get_database_url

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def load_models(DATABASE_URL):
    try:

        engine = create_engine(DATABASE_URL, echo=False)

        Base.metadata.create_all(engine)
        logging.info("All tables successfully loaded into gold schema.")

    except Exception as e:
        logging.error(f"Error loading tables into DB: {e}")


if __name__ == "__main__":
    DATABASE_URL = get_database_url()
    load_models(DATABASE_URL)
