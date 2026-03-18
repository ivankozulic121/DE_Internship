from kafka import KafkaProducer
import json
import requests
import os
from sqlalchemy import text
from data.db import engine
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()

BASE_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")
KAFKA_SERVER = os.getenv("KAFKA_SERVER")


def get_longitudes_and_latitudes():
    with engine.begin() as conn:
        result = conn.execute(text("SELECT lat, long FROM gold.dim_circuits"))
        return result.fetchall()


def fetch_weather_data_to_kafka():

    producer = KafkaProducer(
        bootstrap_servers=KAFKA_SERVER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        key_serializer=lambda k: str(k).encode('utf-8'),
        acks='all',                
        max_in_flight_requests_per_connection=1, 
        enable_idempotence=True     
    )

    towns_data = get_longitudes_and_latitudes()

    for lat, lon in towns_data:

        response = requests.get(
            f"{BASE_URL}?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        )

        data = response.json()
        current_weather = data.get("main")

        if current_weather is None:
            continue

        # Use a unique key for each location (lat-lon combination)
        message_key = f"{lat}-{lon}"

        message = {
            "temperature": current_weather.get("temp"),
            "humidity": current_weather.get("humidity"),
            "pressure": current_weather.get("pressure"),
            "wind_speed": data.get("wind", {}).get("speed"),
            "location": data.get("name")
        }

        producer.send("gold_layer_topic", key=message_key, value=message)

    producer.flush()
    logging.info("Weather data fetched and sent to Kafka")


if __name__ == "__main__":
    fetch_weather_data_to_kafka()