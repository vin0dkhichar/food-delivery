import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY") or "change-me"
    ALGORITHM: str = os.getenv("ALGORITHM") or "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES") or 60
    )

    KAFKA_BROKER: str = os.getenv("KAFKA_BROKER", "localhost:9092")
    KAFKA_TOPIC_ORDERS: str = os.getenv("KAFKA_TOPIC_ORDERS", "orders")


settings = Settings()
