from mailersend import MailerSendClient, EmailBuilder
from app.core.config import settings
from .base_notification import BaseNotificationService
from .registry import NotificationRegistry


class MailerSendEmailService(BaseNotificationService):
    def __init__(self):
        self.api_key = settings.MAILERSEND_API_KEY
        self.from_email = {"name": "Eat Tree", "email": settings.EMAIL_FROM}
        self.mailer = MailerSendClient(api_key=self.api_key)

    def send(self, data: dict):
        recipient_email = data.get("email")
        # recipient_email = "vinodkhichartechno@gmail.com"

        recipient_name = data.get("name")
        email = (
            EmailBuilder()
            .from_email(self.from_email["email"], self.from_email["name"])
            .to_many([{"email": recipient_email, "name": recipient_name}])
            .subject("Notification")
            .html(f"<p>{data.get('message', '')}</p>")
            .text(data.get("message", ""))
            .build()
        )

        try:
            response = self.mailer.emails.send(email)
        except Exception as e:
            print(f"[EMAIL] Failed to send email: {e}")


NotificationRegistry.register("email", MailerSendEmailService)
