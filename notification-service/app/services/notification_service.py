from .registry import NotificationRegistry
from app.core.logger import logger


class NotificationService:
    def __init__(self):
        self.services = NotificationRegistry.all_services()

    def notify_order_created(self, data: dict):
        logger.info(f"Start notifying for order_id={data.get('order_id')}")
        for service in self.services:
            try:
                service.send(data)
            except Exception as e:
                logger.error(
                    f"Error sending notification via {service.__class__.__name__}: {e}"
                )
        logger.info(f"Finished notifying for order_id={data.get('order_id')}")
