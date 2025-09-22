from mailersend import MailerSendClient, EmailBuilder

from app.core.config import settings
from .base_notification import BaseNotificationService
from .registry import NotificationRegistry
from app.core.logger import logger


class MailerSendEmailService(BaseNotificationService):
    def __init__(self):
        self.api_key = settings.MAILERSEND_API_KEY
        self.from_email = {"name": "Eat Tree", "email": settings.EMAIL_FROM}
        self.mailer = MailerSendClient(api_key=self.api_key)

    def send(self, data: dict):
        recipient_name = data.get("name")
        recipient_email = data.get("email")
        subject = data.get("subject")
        message = data.get("message")

        # recipient_email = "vinodkhichartechno@gmail.com"

        if not recipient_email or not message:
            logger.warning(f"[EMAIL] Missing recipient or message: {data}")
            return

        logger.debug(f"[EMAIL] Sending to {recipient_email}: {message}")
        email = (
            EmailBuilder()
            .from_email(self.from_email["email"], self.from_email["name"])
            .to_many([{"email": recipient_email, "name": recipient_name}])
            .subject(subject)
            .text(message)
            .build()
        )

        try:
            self.mailer.emails.send(email)
            logger.info(f"[EMAIL] Sent successfully to {recipient_email}")
        except Exception as e:
            logger.error(f"[EMAIL] Failed to send to {recipient_email}: {e}")


NotificationRegistry.register("email", MailerSendEmailService)
