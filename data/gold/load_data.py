import os
import logging
import sqlalchemy
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# ---------------------------------------------------
# LOAD ENV VARIABLES
# ---------------------------------------------------

load_dotenv()

# ---------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)

# ---------------------------------------------------
# LOGGING
# ---------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------
# DIM DRIVER
# ---------------------------------------------------

def load_dim_driver(conn):
    query = """
    INSERT INTO gold.dim_drivers
    ("driverId", "driverRef", "number", "code", "forename", "surname", "dob", "nationality", "url")
    SELECT DISTINCT
        s."driverId",
        NULLIF(s."driverRef",'\\N'),
        NULLIF(NULLIF(s."number_drivers",'\\N'),'')::int,
        NULLIF(s."code",'\\N'),
        NULLIF(s."forename",'\\N'),
        NULLIF(s."surname",'\\N'),
        NULLIF(NULLIF(s."dob",'\\N'),'')::date,
        NULLIF(s."nationality",'\\N'),
        NULLIF(s."url",'\\N')
    FROM silver.formula1_silver s
    ON CONFLICT ON CONSTRAINT dim_drivers_pkey DO NOTHING
    """
    conn.execute(text(query))

# ---------------------------------------------------
# DIM CONSTRUCTOR
# ---------------------------------------------------

def load_dim_constructor(conn):
    query = """
    INSERT INTO gold.dim_constructors
    ("constructorId", constructorRef", "name", "nationality", "url")
    SELECT DISTINCT
        s."constructorId",
        NULLIF(s."constructorRef",'\\N'),
        NULLIF(s."name",'\\N'),
        NULLIF(s."nationality_constructors",'\\N'),
        NULLIF(s."url_constructors",'\\N')
    FROM silver.formula1_silver s
    ON CONFLICT ON CONSTRAINT dim_constructors_pkey DO NOTHING
    """
    conn.execute(text(query))

# ---------------------------------------------------
# DIM CIRCUIT
# ---------------------------------------------------

def load_dim_circuit(conn):
    query = r"""
    INSERT INTO gold.dim_circuits
    ("circuitId", circuitRef", "name", "location", "country", "lat", "long", "alt", "url")
    SELECT DISTINCT
        s."circuitId",
        NULLIF(s."circuitRef",'\\N'),
        NULLIF(s."name_y",'\\N'),
        NULLIF(s."location",'\\N'),
        NULLIF(s."country",'\\N'),
        NULLIF(NULLIF(s."lat"::text, '\N'), '')::float,
        NULLIF(NULLIF(s."lng"::text, '\N'), '')::float,
        NULLIF(NULLIF(s."alt"::text, '\N'), '')::float
    FROM silver.formula1_silver s
    ON CONFLICT ON CONSTRAINT dim_circuits_pkey DO NOTHING
    """
    conn.execute(text(query))

# ---------------------------------------------------
# DIM RACE
# ---------------------------------------------------

def load_dim_race(conn):
    query = """
    INSERT INTO gold.dim_races
    ("raceId", "year", "round", "name", "time", "url")
    SELECT DISTINCT
        s."raceId",
        NULLIF(NULLIF(s."year"::text,'\\N'),'')::int,
        NULLIF(NULLIF(s."round"::text,'\\N'),'')::int,
        NULLIF(s."name_x",'\\N'),
        NULLIF(NULLIF(s."time_races",'\\N'),'')::time,
        NULLIF(s."url_x",'\\N')
    FROM silver.formula1_silver s
    ON CONFLICT ON CONSTRAINT dim_races_pkey DO NOTHING
    """
    conn.execute(text(query))

# ---------------------------------------------------
# DIM DATE
# ---------------------------------------------------

def load_dim_date(conn):
    query = """
    INSERT INTO gold.dim_date
    ("date", "year", "month", "day", "quarter", "dayOfWeek")
    SELECT DISTINCT
        NULLIF(NULLIF(s."date",'\\N'),'')::date,
        EXTRACT(YEAR FROM NULLIF(NULLIF(s."date",'\\N'),'')::date),
        EXTRACT(MONTH FROM NULLIF(NULLIF(s."date",'\\N'),'')::date),
        EXTRACT(DAY FROM NULLIF(NULLIF(s."date",'\\N'),'')::date),
        EXTRACT(QUARTER FROM NULLIF(NULLIF(s."date",'\\N'),'')::date),
        EXTRACT(DOW FROM NULLIF(NULLIF(s."date",'\\N'),'')::date)
    FROM silver.formula1_silver s
    ON CONFLICT ON CONSTRAINT dim_date_pkey DO NOTHING
    """
    conn.execute(text(query))

# ---------------------------------------------------
# FACT RESULTS
# ---------------------------------------------------

def load_fact_results(conn):
    query = """
    INSERT INTO gold.fact_results
    ("raceId", "driverId", "constructorId", "circuitId", "dateId",
     "carNumber", "grid", "position", "positionText", "positionOrder",
     "points", "laps", "time", "milliseconds",
     "fastestLap", "rank", "fastestLapTime", "fastestLapSpeed")
    SELECT
        r."raceId",
        d."driverId",
        c."constructorId",
        ci."circuitId",
        t."dateId",
        NULLIF(NULLIF(s."number"::text,'\\N'),'')::int,
        NULLIF(NULLIF(s."grid"::text,'\\N'),'')::int,
        NULLIF(NULLIF(s."position"::text,'\\N'),'')::int,
        NULLIF(s."positionText",'\\N'),
        NULLIF(NULLIF(s."positionOrder"::text,'\\N'),'')::int,
        NULLIF(NULLIF(s."points"::text,'\\N'),'')::float,
        NULLIF(NULLIF(s."laps"::text,'\\N'),'')::int,
        NULLIF(s."time"::text,'\\N')::time,
        NULLIF(NULLIF(s."milliseconds"::text,'\\N'),'')::int,
        NULLIF(NULLIF(s."fastestLap",'\\N'),'')::int,
        NULLIF(NULLIF(s."rank"::text,'\\N'),'')::int,
        NULLIF(s."fastestLapTime"::text,'\\N')::time,
        NULLIF(NULLIF(s."fastestLapSpeed",'\\N'),'')::float
    FROM silver.formula1_silver s
    JOIN gold.dim_drivers d ON d."driverRef" = s."driverRef"
    JOIN gold.dim_constructors c ON c."constructorRef" = s."constructorRef"
    JOIN gold.dim_circuits ci ON ci."circuitRef" = s."circuitRef"
    JOIN gold.dim_races r ON r."year" = NULLIF(NULLIF(s."year"::text,'\\N'),'')::int
                      AND r."round" = NULLIF(NULLIF(s."round"::text,'\\N'),'')::int
    JOIN gold.dim_date t ON t.date = NULLIF(NULLIF(s."date"::text,'\\N'),'')::date
    ON CONFLICT DO NOTHING
    """
    conn.execute(text(query))

# ---------------------------------------------------
# MAIN PIPELINE
# ---------------------------------------------------

def run_db_load():
    with engine.begin() as conn:

        logger.info("Starting DB load")

        load_dim_driver(conn)
        load_dim_constructor(conn)
        load_dim_circuit(conn)
        load_dim_race(conn)
        load_dim_date(conn)

        load_fact_results(conn)

        logger.info("DB load finished")

# ---------------------------------------------------

if __name__ == "__main__":
    run_db_load()