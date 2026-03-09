from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class StagingFormula1(Base):
    __tablename__ = "formula1_staging"
    __table_args__ = {"schema": "bronze"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    resultId = Column(Integer)
    raceId = Column(Integer)
    driverId = Column(Integer)
    circuitId = Column(Integer)
    constructorId = Column(Integer)
    number = Column(Integer)
    grid = Column(Integer)
    position = Column(String)
    positionText = Column(String)
    positionOrder = Column(Integer)
    points = Column(Float)
    laps = Column(Integer)
    time = Column(String)
    milliseconds = Column(String)
    fastestLap = Column(String)
    rank = Column(Integer)
    fastestLapTime = Column(String)
    fastestLapSpeed = Column(String)
    statusId = Column(Integer)
    year = Column(Integer)
    round = Column(Integer)
    name_x = Column(String)
    date = Column(String)
    time_races = Column(String)
    url_x = Column(String)
    fp1_date = Column(String)
    fp1_time = Column(String)
    fp2_date = Column(String)
    fp2_time = Column(String)
    fp3_date = Column(String)
    fp3_time = Column(String)
    quali_date = Column(String)
    quali_time = Column(String)
    sprint_date = Column(String)
    sprint_time = Column(String)
    circuitRef = Column(String)
    name_y = Column(String)
    location = Column(String)
    country = Column(String)
    lat = Column(Float)
    lng = Column(Float)
    alt = Column(String)
    url_y = Column(String)
    driverRef = Column(String)
    number_drivers = Column(String)
    code = Column(String)
    forename = Column(String)
    surname = Column(String)
    dob = Column(String)
    nationality = Column(String)
    url = Column(String)
    constructorRef = Column(String)
    name = Column(String)
    nationality_constructors = Column(String)
    url_constructors = Column(String)
    lap = Column(Integer)
    position_laptimes = Column(Integer)
    time_laptimes = Column(String)
    milliseconds_laptimes = Column(Integer)
    stop = Column(Integer)
    lap_pitstops = Column(Integer)
    time_pitstops = Column(String)
    duration = Column(String)
    milliseconds_pitstops = Column(Integer)
    driverStandingsId = Column(Integer)
    points_driverstandings = Column(Float)
    position_driverstandings = Column(Integer)
    positionText_driverstandings = Column(Integer)
    wins = Column(Integer)
    constructorStandingsId = Column(Integer)
    points_constructorstandings = Column(Float)
    position_constructorstandings = Column(Integer)
    positionText_constructorstandings = Column(Integer)
    wins_constructorstandings = Column(Integer)
    status = Column(String)



    import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import text
#from config import engine
import os
import logging
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

try: 
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10
    )

except Exception as e:
    print(f"Error connecting to DB: {e}")
# ---------------------------------------------------
# LOGGING SETUP  (NOVO)
# ---------------------------------------------------

# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s | %(levelname)s | %(message)s"
# )

# logger = logging.getLogger(__name__)

# # ---------------------------------------------------
# # GET ALL BATCHES
# # ---------------------------------------------------

# def get_new_batches(conn):
#     query = """
#     SELECT batch_id
#     FROM staging.control_f1
#     ORDER BY load_date
#     """
#     return [row[0] for row in conn.execute(text(query))]


# # ---------------------------------------------------
# # DIM DRIVER
# # ---------------------------------------------------

# def load_dim_driver(conn, batch_id):
#     query = """
#     INSERT INTO gold.dim_drivers
#     (driverRef, number, code, forename, surname, dob, nationality, url)
#     SELECT DISTINCT
#         NULLIF(s."driverRef",'\\N'),
#         NULLIF(NULLIF(s."number_drivers",'\\N'),'')::int,
#         NULLIF(s."code",'\\N'),
#         NULLIF(s."forename",'\\N'),
#         NULLIF(s."surname",'\\N'),
#         NULLIF(NULLIF(s."dob",'\\N'),'')::date,
#         NULLIF(s."nationality",'\\N'),
#         NULLIF(s."url",'\\N')
#     FROM silver.formula1_silver s
#     WHERE s.batch_id = :batch_id
#     ON CONFLICT (driverRef) DO NOTHING
#     """
#     conn.execute(text(query), {"batch_id": batch_id})


# # ---------------------------------------------------
# # DIM CONSTRUCTOR
# # ---------------------------------------------------

# def load_dim_constructor(conn, batch_id):
#     query = """
#     INSERT INTO gold.dim_constructors
#     (constructorRef, name, nationality, url)
#     SELECT DISTINCT
#         NULLIF(s."constructorRef",'\\N'),
#         NULLIF(s."name",'\\N'),
#         NULLIF(s."nationality_constructors",'\\N'),
#         NULLIF(s."url_constructors",'\\N')
#     FROM silver.formula1_silver s
#     WHERE s.batch_id = :batch_id
#     ON CONFLICT (constructorRef) DO NOTHING
#     """
#     conn.execute(text(query), {"batch_id": batch_id})


# # ---------------------------------------------------
# # DIM CIRCUIT
# # ---------------------------------------------------

# def load_dim_circuit(conn, batch_id):
#     query = """
#     INSERT INTO gold.dim_circuits
#     (circuitRef, name, location, country, lat, long, alt, url)
#     SELECT DISTINCT
#         NULLIF(s."circuitRef",'\\N'),
#         NULLIF(s."name_y",'\\N'),
#         NULLIF(s."location",'\\N'),
#         NULLIF(s."country",'\\N'),
#         NULLIF(NULLIF(s."lat",'\\N'),'')::float,
#         NULLIF(NULLIF(s."lng",'\\N'),'')::float,
#         NULLIF(NULLIF(s."alt",'\\N'),'')::float,
#         NULLIF(s."url_y",'\\N')
#     FROM silver.formula1_silver s 
#     WHERE s.batch_id = :batch_id
#     ON CONFLICT (circuit_ref) DO NOTHING
#     """
#     conn.execute(text(query), {"batch_id": batch_id})


# # ---------------------------------------------------
# # DIM RACE
# # ---------------------------------------------------

# def load_dim_race(conn, batch_id):
#     query = """
#     INSERT INTO gold.dim_races
#     (year, round, name, time, url)
#     SELECT DISTINCT
#         NULLIF(NULLIF(s."year",'\\N'),'')::int,
#         NULLIF(NULLIF(s."round",'\\N'),'')::int,
#         NULLIF(s."name_x",'\\N'),
#         NULLIF(NULLIF(s."time_races",'\\N'),'')::time,
#         NULLIF(s."url_x",'\\N')
#     FROM silver.formula1_silver s
#     WHERE s.batch_id = :batch_id
#     ON CONFLICT (year, round) DO NOTHING
#     """
#     conn.execute(text(query), {"batch_id": batch_id})


# # ---------------------------------------------------
# # DIM TIME
# # ---------------------------------------------------

# def load_dim_date(conn, batch_id):
#     query = """
#     INSERT INTO gold.dim_date
#     (date, year, month, day, quarter, dayOfWeek)
#     SELECT DISTINCT
#         NULLIF(NULLIF(s."date",'\\N'),'')::date,
#         EXTRACT(YEAR FROM NULLIF(NULLIF(s."date",'\\N'),'')::date),
#         EXTRACT(MONTH FROM NULLIF(NULLIF(s."date",'\\N'),'')::date),
#         EXTRACT(DAY FROM NULLIF(NULLIF(s."date",'\\N'),'')::date),
#         EXTRACT(QUARTER FROM NULLIF(NULLIF(s."date",'\\N'),'')::date),
#         EXTRACT(DOW FROM NULLIF(NULLIF(s."date",'\\N'),'')::date)
#     FROM silver.formula1_silver s
#     WHERE s.batch_id = :batch_id
#     ON CONFLICT (date) DO NOTHING
#     """
#     conn.execute(text(query), {"batch_id": batch_id})


# # ---------------------------------------------------
# # FACT RACE RESULTS
# # ---------------------------------------------------

# def load_fact_results(conn, batch_id):
#     query = """
#     INSERT INTO gold.fact_results
#     (raceId, driverId, constructorId, circuitId, dateId,
#      carNumber, grid, position, positionText, positionOrder,
#      points, laps, time, milliseconds,
#      fastestLap, rank, fastestLapTime, fastestLapSpeed)
#     SELECT
#         r.raceId,
#         d.driverId,
#         c.constructorId,
#         ci.circuitId,
#         t.dateId,
#         NULLIF(NULLIF(s."number",'\\N'),'')::int,
#         NULLIF(NULLIF(s."grid",'\\N'),'')::int,
#         NULLIF(NULLIF(s."position",'\\N'),'')::int,
#         NULLIF(s."positionText",'\\N'),
#         NULLIF(NULLIF(s."positionOrder",'\\N'),'')::int,
#         NULLIF(NULLIF(s."points",'\\N'),'')::float,
#         NULLIF(NULLIF(s."laps",'\\N'),'')::int,
#         NULLIF(s."time",'\\N'),
#         NULLIF(NULLIF(s."milliseconds",'\\N'),'')::int,
#         NULLIF(NULLIF(s."fastestLap",'\\N'),'')::int,
#         NULLIF(NULLIF(s."rank",'\\N'),'')::int,
#         NULLIF(s."fastestLapTime",'\\N'),
#         NULLIF(NULLIF(s."fastestLapSpeed",'\\N'),'')::float
#     FROM silver.formula1_silver s
#     JOIN gold.dim_drivers d ON d.driverRef = s."driverRef"
#     JOIN gold.dim_constructors c ON c.constructorRef = s."constructorRef"
#     JOIN gold.dim_circuits ci ON ci.circuitRef = s."circuitRef"
#     JOIN gold.dim_races r ON r.year = NULLIF(NULLIF(s."year",'\\N'),'')::int
#                       AND r.round = NULLIF(NULLIF(s."round",'\\N'),'')::int
#     JOIN gold.dim_date t ON t.date = NULLIF(NULLIF(s."date",'\\N'),'')::date
#     WHERE s.batch_id = :batch_id
#     ON CONFLICT DO NOTHING
#     """
#     conn.execute(text(query), {"batch_id": batch_id})


# # ---------------------------------------------------
# # FACT PIT STOPS
# # ---------------------------------------------------

# def load_fact_pit_stops(conn, batch_id):
#     query = """
#     INSERT INTO gold.fact_pit_stops
#     (raceId, driverId, constructorId, circuitId, dateId,
#      stop_number, lap, pit_time, duration, duration_ms)
#     SELECT
#         r.race_id,
#         d.driver_id,
#         c.constructor_id,
#         ci.circuit_id,
#         t.time_id,
#         NULLIF(NULLIF(s."stop",'\\N'),'')::int,
#         NULLIF(NULLIF(s."lap_pitstops",'\\N'),'')::int,
#         NULLIF(s."time_pitstops",'\\N'),
#         NULLIF(s."duration",'\\N'),
#         NULLIF(NULLIF(s."milliseconds_pitstops",'\\N'),'')::int
#     FROM silver.formula1_silver s
#     JOIN gold.dim_drivers d ON d.driverRef = s."driverRef"
#     JOIN gold.dim_constructors c ON c.constructorRef = s."constructorRef"
#     JOIN gold.dim_circuits ci ON ci.circuitRef = s."circuitRef"
#     JOIN gold.dim_races r ON r.year = NULLIF(NULLIF(s."year",'\\N'),'')::int
#                       AND r.round = NULLIF(NULLIF(s."round",'\\N'),'')::int
#     JOIN gold.dim_date t ON t.date = NULLIF(NULLIF(s."date",'\\N'),'')::date
#     WHERE s.batch_id = :batch_id AND s."stop" IS NOT NULL
#     ON CONFLICT DO NOTHING
#     """
#     conn.execute(text(query), {"batch_id": batch_id})


# # ---------------------------------------------------
# # FACT LAP TIMES
# # ---------------------------------------------------

# def load_fact_lap_times(conn, batch_id):
#     query = """
#     INSERT INTO gold.fact_lap_times
#     (raceId, driverId, constructorId, circuitId, dateId,
#      lap_number, position_in_lap, lap_time, lap_time_ms)
#     SELECT
#         r.raceId,
#         d.driverId,
#         c.constructorId,
#         ci.circuitId,
#         t.dateId,
#         NULLIF(NULLIF(s."lap",'\\N'),'')::int,
#         NULLIF(NULLIF(s."position_laptimes",'\\N'),'')::int,
#         NULLIF(s."time_laptimes",'\\N'),
#         NULLIF(NULLIF(s."milliseconds_laptimes",'\\N'),'')::int
#     FROM staging.staging_f1 s
#     JOIN gold.dim_drivers d ON d.driver_ref = s."driverRef"
#     JOIN gold.dim_constructors c ON c.constructor_ref = s."constructorRef"
#     JOIN gold.dim_circuits ci ON ci.circuit_ref = s."circuitRef"
#     JOIN gold.dim_races r ON r.year = NULLIF(NULLIF(s."year",'\\N'),'')::int
#                       AND r.round = NULLIF(NULLIF(s."round",'\\N'),'')::int
#     JOIN dw.dim_date t ON t.date = NULLIF(NULLIF(s."date",'\\N'),'')::date
#     WHERE s.batch_id = :batch_id AND s."lap" IS NOT NULL
#     ON CONFLICT DO NOTHING
#     """
#     conn.execute(text(query), {"batch_id": batch_id})


# # ---------------------------------------------------
# # MAIN PIPELINE
# # ---------------------------------------------------

# def run_dw_load():
#     with engine.begin() as conn:

#             logger.info(f"Processing batch {batch}")
#             load_dim_driver(conn, batch)
#             load_dim_constructor(conn, batch)
#             load_dim_circuit(conn, batch)
#             load_dim_race(conn, batch)
#             load_dim_date(conn, batch)
#             load_fact_results(conn, batch)
#             load_fact_pit_stops(conn, batch)
#             load_fact_lap_times(conn, batch)
#             logger.info(f"Batch {batch} finished")


# if __name__ == "__main__":
#     run_dw_load()