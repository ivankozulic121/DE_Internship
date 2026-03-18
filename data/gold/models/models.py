from sqlalchemy import Column, Integer, String, Float, Date, Time, DECIMAL, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Result(Base):
    __tablename__ = "fact_results"
    __table_args__ = {"schema": "gold"}

    resultId = Column(Integer, primary_key=True)
    raceId = Column(Integer, ForeignKey("gold.dim_races.raceId"))
    driverId = Column(Integer, ForeignKey("gold.dim_drivers.driverId"))
    constructorId = Column(Integer, ForeignKey("gold.dim_constructors.constructorId"))
    circuitId = Column(Integer, ForeignKey("gold.dim_circuits.circuitId"))
    dateId = Column(Integer, ForeignKey("gold.dim_date.date"))
    carNumber = Column(Integer)
    grid = Column(Integer)
    position = Column(Integer)
    positionText = Column(String)
    positionOrder = Column(Integer)
    points = Column(Integer)
    laps = Column(Integer)
    time = Column(Time)
    milliseconds = Column(String)
    fastestLap = Column(Integer)
    rank = Column(Integer)
    fastestLapTime = Column(Time)
    fastestLapSpeed = Column(DECIMAL)
    statusID = Column(String)

    driver = relationship("Driver", back_populates="results")
    constructor = relationship("Constructor", back_populates="results")
    circuit = relationship("Circuit", back_populates="results")
    date = relationship("Date", back_populates="results")
    race = relationship("Race", back_populates="results")


class Driver(Base):
    __tablename__ = "dim_drivers"
    __table_args__ = {"schema": "gold"}

    driverId = Column(Integer, primary_key=True)
    driverRef = Column(String)
    number = Column(Integer)
    code = Column(String)
    forename = Column(String)
    surname = Column(String)
    dob = Column(Date)
    nationality = Column(String)
    url = Column(String)

    results = relationship("Result", back_populates="driver")
    pit_stops = relationship("PitStop", back_populates="driver")
    lap_times = relationship("LapTime", back_populates="driver")


class Race(Base):
    __tablename__ = "dim_races"
    __table_args__ = {"schema": "gold"}

    raceId = Column(Integer, primary_key=True)
    year = Column(Integer)
    round = Column(Integer)
    name = Column(String)
    time = Column(Time)
    url = Column(String)

    results = relationship("Result", back_populates="race")
    pit_stops = relationship("PitStop", back_populates="race")
    lap_times = relationship("LapTime", back_populates="race")


class Circuit(Base):
    __tablename__ = "dim_circuits"
    __table_args__ = {"schema": "gold"}

    circuitId = Column(Integer, primary_key=True)
    circuitRef = Column(String)
    name = Column(String)
    location = Column(String)
    country = Column(String)
    lat = Column(DECIMAL)
    long = Column(DECIMAL)
    alt = Column(Integer)
    url = Column(String)

    results = relationship("Result", back_populates="circuit")


class Constructor(Base):
    __tablename__ = "dim_constructors"
    __table_args__ = {"schema": "gold"}

    constructorId = Column(Integer, primary_key=True)
    constructorRef = Column(String)
    name = Column(String)
    nationality = Column(String)
    url = Column(String)

    results = relationship("Result", back_populates="constructor")


class Date(Base):
    __tablename__ = "dim_date"
    __table_args__ = {"schema": "gold"}

    date = Column(Integer, primary_key=True)
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)
    quarter = Column(Integer)
    dayOfWeek = Column(Integer)

    results = relationship("Result", back_populates="date")


class PitStop(Base):
    __tablename__ = "fact_pit_stops"
    __table_args__ = {"schema": "gold"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    driverId = Column(Integer, ForeignKey("gold.dim_drivers.driverId"))
    raceId = Column(Integer, ForeignKey("gold.dim_races.raceId"))
    stop = Column(String)
    lap = Column(Integer)
    time = Column(Time)
    duration = Column(DECIMAL)
    milliseconds = Column(Integer)

    driver = relationship("Driver", back_populates="pit_stops")
    race = relationship("Race", back_populates="pit_stops")


class LapTime(Base):
    __tablename__ = "fact_lap_times"
    __table_args__ = {"schema": "gold"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    driverId = Column(Integer, ForeignKey("gold.dim_drivers.driverId"))
    raceId = Column(Integer, ForeignKey("gold.dim_races.raceId"))
    stop = Column(String)
    lap = Column(Integer)
    position = Column(Integer)
    time = Column(Time)
    milliseconds = Column(Integer)

    driver = relationship("Driver", back_populates="lap_times")
    race = relationship("Race", back_populates="lap_times")


class Weather(Base):
    __tablename__ = "current_weather_forecast"
    __table_args__ = {"schema": "gold"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    temperature = Column(DECIMAL)
    humidity = Column(Integer)
    pressure = Column(Integer)
    wind_speed = Column(DECIMAL)
    location = Column(String)