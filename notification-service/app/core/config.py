import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    KAFKA_BROKER: str = os.getenv("KAFKA_BROKER", "localhost:9092")
    KAFKA_TOPIC_ORDERS: str = os.getenv("KAFKA_TOPIC_ORDERS", "orders")
    GROUP_ID: str = "notification_service"

    MAILERSEND_API_KEY: str = os.getenv("MAILERSEND_API_KEY")
    EMAIL_FROM: str = os.getenv("EMAIL_FROM")

    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER: str = os.getenv("TWILIO_PHONE_NUMBER")


settings = Settings()
