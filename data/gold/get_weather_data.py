import requests
import os
import json
from sqlalchemy import text
from data.db import engine
from dotenv import load_dotenv
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

load_dotenv()

BASE_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")


def get_longitudes_and_latitudes():
    with engine.begin() as conn:
        query = "SELECT lat, long from gold.dim_circuits"
        result = conn.execute(text(query))
    
        return result.fetchall()
    
def fetch_weather_data():
    towns_data = get_longitudes_and_latitudes()

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE gold.current_weather_forecast RESTART IDENTITY"))
        for lat,lon in towns_data:
            response = requests.get(f"{BASE_URL}?lat={lat}&lon={lon}&appid={API_KEY}&units=metric")
            data = response.json()
            current_weather = data.get("main")
            
            if current_weather is None:
                    print(f"Error for {lat},{lon}: {data}")
                    continue

            wind_speed = data.get("wind", {}).get("speed")
            location = data.get("name")

            conn.execute(text("""
                    INSERT INTO gold.current_weather_forecast (
                        temperature,
                        humidity,
                        pressure,
                        wind_speed,
                        location
                    )
                    VALUES (:temperature, :humidity, :pressure, :wind_speed, :location)
                """), {
                    "temperature": current_weather.get("temp"),
                    "humidity": current_weather.get("humidity"),
                    "pressure": current_weather.get("pressure"),
                    "wind_speed": wind_speed,
                    "location": location
                })
            
        logging.info("Weather data successfully fetched into database")

    

if __name__ == "__main__":
    fetch_weather_data()


