import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    KAFKA_BROKER: str = os.getenv("KAFKA_BROKER", "localhost:9092")
    KAFKA_TOPIC_ORDERS: str = os.getenv("KAFKA_TOPIC_ORDERS", "orders")
    GROUP_ID: str = "notification_service"


settings = Settings()
