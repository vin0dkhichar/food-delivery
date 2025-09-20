from kafka import KafkaProducer
import json
from app.core.config import settings

producer = KafkaProducer(
    bootstrap_servers=settings.KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


def send_order_created_event(order_data: dict):
    producer.send(settings.KAFKA_TOPIC_ORDERS, order_data)
    producer.flush()
