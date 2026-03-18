from kafka import KafkaConsumer
import json
from sqlalchemy import text
from data.db import engine
from dotenv import load_dotenv
import logging
import os

logging.basicConfig(level=logging.INFO)

load_dotenv()

KAFKA_SERVER = os.getenv("KAFKA_SERVER")

def load_weather_data_to_db():

    consumer = KafkaConsumer(
        'gold_layer_topic',
        bootstrap_servers=KAFKA_SERVER,
        auto_offset_reset='earliest',
        enable_auto_commit=False,
        group_id="weather_consumer_group",
        consumer_timeout_ms=5000,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE gold.current_weather_forecast RESTART IDENTITY"))

        for message in consumer:
            data = message.value

            conn.execute(text("""
                INSERT INTO gold.current_weather_forecast (
                    temperature, humidity, pressure, wind_speed, location
                )
                VALUES (:temperature, :humidity, :pressure, :wind_speed, :location)
            """), data)

            consumer.commit()
        logging.info("Data successfully loaded from Kafka")


if __name__ == "__main__":
    load_weather_data_to_db()