from cryptography.fernet import Fernet
from django.conf import settings


class Hashing:
    __secret: str = settings.SECRET
    __fernet = Fernet(__secret)

    @classmethod
    def encrypt(cls, message: str):
        encrypted_message = cls.__fernet.encrypt(message.encode())
        return encrypted_message.decode()

    @classmethod
    def decrypt(cls, message: bytes) -> str:
        return cls.__fernet.decrypt(message).decode()
