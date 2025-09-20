from kafka import KafkaConsumer
import json
from app.services.notification_service import NotificationService
from app.core.config import settings

consumer = KafkaConsumer(
    settings.KAFKA_TOPIC_ORDERS,
    bootstrap_servers=settings.KAFKA_BROKER,
    group_id=settings.GROUP_ID,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
)

service = NotificationService()


def consume_order_events():
    for event_data in consumer:
        service.notify_order_created(event_data.value)
