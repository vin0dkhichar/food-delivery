from abc import ABC, abstractmethod


class BaseNotificationService(ABC):
    @abstractmethod
    def send(self, data: dict):
        """Send a notification."""
        pass
