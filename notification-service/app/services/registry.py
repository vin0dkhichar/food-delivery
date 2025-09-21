from typing import Type
from .base_notification import BaseNotificationService


class NotificationRegistry:
    _services = {}

    @classmethod
    def register(cls, name: str, service: Type[BaseNotificationService]):
        """Register a service by name."""
        cls._services[name] = service()

    @classmethod
    def get_service(cls, name: str) -> BaseNotificationService:
        """Get a registered service."""
        return cls._services.get(name)

    @classmethod
    def all_services(cls):
        """Return all registered services."""
        return list(cls._services.values())
