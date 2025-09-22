import json
from kafka import KafkaConsumer

from app.services.notification_service import NotificationService
from app.core.config import settings
from app.core.logger import logger


consumer = KafkaConsumer(
    settings.KAFKA_TOPIC_ORDERS,
    bootstrap_servers=settings.KAFKA_BROKER,
    group_id=settings.GROUP_ID,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
)

service = NotificationService()


def consume_order_events():
    logger.info("Started consuming Kafka order events...")
    for event_data in consumer:
        logger.debug(f"Received event: {event_data.value}")
        try:
            service.notify_order_created(event_data.value)
        except Exception as e:
            logger.error(f"Error processing event {event_data.value}: {e}")
    logger.info("Stopped consuming Kafka order events.")
