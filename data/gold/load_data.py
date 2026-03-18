import logging
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from data.db import engine

# ---------------------------------------------------
# LOAD ENV VARIABLES
# ---------------------------------------------------

load_dotenv()

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

def load_dim_drivers():
    with engine.begin() as conn:
        query = """
        INSERT INTO gold.dim_drivers
        ("driverId", "driverRef", "number", "code", "forename", "surname", "dob", "nationality", "url")
        SELECT DISTINCT
            s."driverId"::int,
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
        logger.info("Table dim_drivers loaded successfully.")

# ---------------------------------------------------
# DIM CONSTRUCTOR
# ---------------------------------------------------

def load_dim_constructors():
    with engine.begin() as conn:
        query = """
        INSERT INTO gold.dim_constructors
        ("constructorId", "constructorRef", "name", "nationality", "url")
        SELECT DISTINCT
            s."constructorId"::int,
            NULLIF(s."constructorRef",'\\N'),
            NULLIF(s."name",'\\N'),
            NULLIF(s."nationality_constructors",'\\N'),
            NULLIF(s."url_constructors",'\\N')
        FROM silver.formula1_silver s
        ON CONFLICT ON CONSTRAINT dim_constructors_pkey DO NOTHING
        """
        conn.execute(text(query))
        logger.info("Table dim_constructors loaded successfully.")

# ---------------------------------------------------
# DIM CIRCUIT
# ---------------------------------------------------

def load_dim_circuits():
     with engine.begin() as conn:
        query = r"""
        INSERT INTO gold.dim_circuits
        ("circuitId", "circuitRef", "name", "location", "country", "lat", "long", "alt", "url")
        SELECT DISTINCT
            s."circuitId"::int,
            NULLIF(s."circuitRef",'\\N'),
            NULLIF(s."name_y",'\\N'),
            NULLIF(s."location",'\\N'),
            NULLIF(s."country",'\\N'),
            NULLIF(NULLIF(s."lat"::text, '\\N'), '')::float,
            NULLIF(NULLIF(s."lng"::text, '\\N'), '')::float,
            NULLIF(NULLIF(s."alt"::text, '\\N'), '')::int,
            NULLIF(s."url_y"::text,'\\N')
        FROM silver.formula1_silver s
        ON CONFLICT ON CONSTRAINT dim_circuits_pkey DO NOTHING
        """
        conn.execute(text(query))
        logger.info("Table dim_circuits loaded successfully.")

# ---------------------------------------------------
# DIM RACE
# ---------------------------------------------------

def load_dim_races():
    with engine.begin() as conn:
        query = """
        INSERT INTO gold.dim_races
        ("raceId", "year", "round", "name", "time", "url")
        SELECT DISTINCT
            s."raceId"::int,
            NULLIF(NULLIF(s."year"::text,'\\N'),'')::int,
            NULLIF(NULLIF(s."round"::text,'\\N'),'')::int,
            NULLIF(s."name_x",'\\N'),
            NULLIF(NULLIF(s."time_races",'\\N'),'')::time,
            NULLIF(s."url_x",'\\N')
        FROM silver.formula1_silver s
        ON CONFLICT ON CONSTRAINT dim_races_pkey DO NOTHING
        """
        conn.execute(text(query))
        logger.info("Table dim_races loaded successfully.")

# ---------------------------------------------------
# DIM DATE
# ---------------------------------------------------

def load_dim_date():
    with engine.begin() as conn:
        query = r"""
        INSERT INTO gold.dim_date
        ("date", "year", "month", "day", "quarter", "dayOfWeek")
        SELECT DISTINCT
            TO_CHAR(NULLIF(NULLIF(s."date"::text,'\\N'),'')::date, 'YYYYMMDD')::integer,
            EXTRACT(YEAR FROM NULLIF(NULLIF(s."date"::text,'\\N'),'')::date),
            EXTRACT(MONTH FROM NULLIF(NULLIF(s."date"::text,'\\N'),'')::date),
            EXTRACT(DAY FROM NULLIF(NULLIF(s."date"::text,'\\N'),'')::date),
            EXTRACT(QUARTER FROM NULLIF(NULLIF(s."date"::text,'\\N'),'')::date),
            EXTRACT(DOW FROM NULLIF(NULLIF(s."date"::text,'\\N'),'')::date)
        FROM silver.formula1_silver s
        ON CONFLICT ON CONSTRAINT dim_date_pkey DO NOTHING
        """
        conn.execute(text(query))
        logger.info("Table dim_date loaded successfully.")

# ---------------------------------------------------
# FACT RESULTS
# ---------------------------------------------------

def load_fact_results():
    with engine.begin() as conn:
        query = r"""
        INSERT INTO gold.fact_results
        ("resultId", "raceId", "driverId", "constructorId", "circuitId", "dateId",
        "carNumber", "grid", "position", "positionText", "positionOrder",
        "points", "laps", "time", "milliseconds",
        "fastestLap", "rank", "fastestLapTime", "fastestLapSpeed")
        SELECT
            s."resultId"::int,
            r."raceId"::int,
            d."driverId"::int,
            c."constructorId"::int,
            ci."circuitId"::int,
            t."date",
            NULLIF(NULLIF(s."number"::text,'\\N'),'')::int,
            NULLIF(NULLIF(s."grid"::text,'\\N'),'')::int,
            NULLIF(NULLIF(s."position"::text,'\\N'),'')::int,
            NULLIF(s."positionText",'\\N'),
            NULLIF(NULLIF(s."positionOrder"::text,'\\N'),'')::int,
            NULLIF(NULLIF(s."points"::text,'\\N'),'')::float::int,
            NULLIF(NULLIF(s."laps"::text,'\\N'),'')::int,
            NULLIF(NULLIF(s."time"::text, '\\N'), '')::time,
            NULLIF(NULLIF(s."milliseconds"::text,'\\N'),'')::float::int,
            NULLIF(NULLIF(s."fastestLap",'\\N'),'')::int,
            NULLIF(NULLIF(s."rank"::text,'\\N'),'')::int,
            NULLIF(NULLIF(s."fastestLapTime"::text, '\\N'), '')::time,
            NULLIF(NULLIF(s."fastestLapSpeed",'\\N'),'')::float
        FROM silver.formula1_silver s
        JOIN gold.dim_drivers d ON d."driverRef" = s."driverRef"
        JOIN gold.dim_constructors c ON c."constructorRef" = s."constructorRef"
        JOIN gold.dim_circuits ci ON ci."circuitRef" = s."circuitRef"
        JOIN gold.dim_races r ON r."year" = NULLIF(NULLIF(s."year"::text,'\\N'),'')::int
                        AND r."round" = NULLIF(NULLIF(s."round"::text,'\\N'),'')::int
        JOIN gold.dim_date t ON t.date = TO_CHAR(NULLIF(NULLIF(s."date"::text,'\\N'),'')::date, 'YYYYMMDD')::integer
        ON CONFLICT DO NOTHING
        """
        conn.execute(text(query))
        logger.info("Table fact_results loaded successfully.")

    # ---------------------------------------------------
    # FACT PIT STOPS
    # ---------------------------------------------------

def load_fact_pit_stops():
    with engine.begin() as conn:
            query = """
            INSERT INTO gold.fact_pit_stops
            ("raceId", "driverId", "stop", "lap", "time", "duration", "milliseconds")
            SELECT
                r."raceId"::int,
                d."driverId"::int,
                NULLIF(NULLIF(s."stop"::text,'\\N'),'')::int,
                NULLIF(NULLIF(s."lap_pitstops"::text,'\\N'),'')::int,
                NULLIF(NULLIF(s."time_pitstops"::text, '\\N'), '')::time,
                NULLIF(s."duration"::text,'\\N')::float,
                NULLIF(NULLIF(s."milliseconds_pitstops"::text,'\\N'),'')::float::int
            FROM silver.formula1_silver s
            JOIN gold.dim_drivers d ON d."driverRef" = s."driverRef"
            JOIN gold.dim_races r ON r.year = NULLIF(NULLIF(s."year"::text,'\\N'),'')::int
                                AND r.round = NULLIF(NULLIF(s."round"::text,'\\N'),'')::int
            ON CONFLICT DO NOTHING
            """
            conn.execute(text(query))
            logger.info("Table fact_pit_stops loaded successfully.")

# ---------------------------------------------------
# FACT LAP TIMES
# ---------------------------------------------------

def load_fact_lap_times():
    with engine.begin() as conn:
        query = """
        INSERT INTO gold.fact_lap_times
        ("raceId", "driverId", "stop", "lap", "position", "time", "milliseconds")
        SELECT
            r."raceId",
            d."driverId",
            NULLIF(NULLIF(s."stop"::text, '\\N'),'')::int,
            NULLIF(NULLIF(s."lap"::text,'\\N'),'')::int,
            NULLIF(NULLIF(s."position_laptimes"::text,'\\N'),'')::int,
            NULLIF(NULLIF(s."time_laptimes"::text, '\\N'), '')::time,
            NULLIF(NULLIF(s."milliseconds_laptimes"::text,'\\N'),'')::float::int
        FROM silver.formula1_silver s
        JOIN gold.dim_drivers d ON d."driverId" = s."driverId"::int
        JOIN gold.dim_races r ON r."raceId" = s."raceId"::int
        GROUP BY
        r."raceId",
        d."driverId",
        s."stop",
        s."lap",
        s."position_laptimes",
        s."time_laptimes",
        s."milliseconds_laptimes"
        ON CONFLICT DO NOTHING;
        """
        conn.execute(text(query))
        logger.info("Table fact_lap_times loaded successfully.")


# ---------------------------------------------------
# MAIN PIPELINE
# ---------------------------------------------------

def run_db_load(engine):
    with engine.begin() as conn:

        logger.info("Starting DB load")

        load_dim_drivers()
        load_dim_constructors()
        load_dim_circuits()
        load_dim_races()
        load_dim_date()
        load_fact_results()
        load_fact_pit_stops()
        load_fact_lap_times()

        logger.info("DB load finished")

# ---------------------------------------------------

if __name__ == "__main__":
    run_db_load(engine)