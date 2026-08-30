from abc import ABC, abstractmethod

class Notification(ABC):
    @abstractmethod
    def send(self, message: str, recipient: str) -> str:
        pass

class EmailNotification(Notification):
    def send(self, message: str, recipient: str) -> str:
        return f"Enviando Email a {recipient}: {message}"

class SMSNotification(Notification):
    def send(self, message: str, recipient: str) -> str:
        return f"Enviando SMS a {recipient}: {message}"

class NotificationFactory:
    @staticmethod
    def get_notifier(notification_type: str) -> Notification:
        if notification_type.lower() == "email":
            return EmailNotification()
        elif notification_type.lower() == "sms":
            return SMSNotification()
        else:
            raise ValueError("Tipo de notificación no soportado.")