from twilio.rest import Client

from .base_notification import BaseNotificationService
from .registry import NotificationRegistry
from app.core.config import settings
from app.core.logger import logger


class SMSService(BaseNotificationService):
    def __init__(self):
        self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        self.from_ = settings.TWILIO_PHONE_NUMBER

    def send(self, data: dict):
        phone = data.get("phone_number")
        msg = data.get("message")

        if not phone or not msg:
            logger.warning(f"[SMS] Missing phone or message: {data}")
            return

        logger.debug(f"[SMS] Sending to {phone}: {msg}")
        # phone = "+18777804236"
        try:
            message = self.client.messages.create(
                body=msg,
                from_=self.from_,
                to=phone,
            )
            logger.info(f"[SMS] Sent successfully to {phone}: {message.body}")
        except Exception as e:
            logger.error(f"[SMS] Failed to send to {phone}: {e}")


NotificationRegistry.register("sms", SMSService)
