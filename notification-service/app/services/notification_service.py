from .registry import NotificationRegistry


class NotificationService:
    def __init__(self):
        self.services = NotificationRegistry.all_services()

    def notify_order_created(self, data: dict):
        for service in self.services:
            service.send(data)
