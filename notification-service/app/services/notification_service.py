class NotificationService:
    def notify_order_created(self, data: dict):
        # Here you can integrate with email/SMS providers
        print(f"[EMAIL] To: {data['email']}, Message: {data['message']}")
        print(f"[SMS] To: {data['phone_number']}, Message: {data['message']}")
