from .base_notification import BaseNotificationService
from .registry import NotificationRegistry


class SMSService(BaseNotificationService):
    def send(self, data: dict):
        phone = data.get("phone_number", "N/A")
        message = data.get("message", "")
        print(f"[SMS] To: {phone}, Message: {message}")


NotificationRegistry.register("sms", SMSService)
