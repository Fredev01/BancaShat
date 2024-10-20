import os
from cryptography.fernet import Fernet


def get_path_key() -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    keys_dir = os.path.join(current_dir, '..', 'keys')
    aes_key_path = os.path.join(keys_dir, 'aes_key.key')
    return aes_key_path


def generate_key() -> None:
    key = Fernet.generate_key()
    with open(get_path_key(), 'wb') as key_file:
        key_file.write(key)


class AESEncrypt:

    @staticmethod
    def load_key(path: str) -> bytes:
        with open(path, 'rb') as key_file:
            return key_file.read()

    def __init__(self) -> None:
        self.key = self.load_key(get_path_key())
        self.fernet = Fernet(self.key)

    def encrypt(self, message: str) -> bytes:
        return self.fernet.encrypt(message.encode())

    def decrypt(self, token: bytes) -> str:
        return self.fernet.decrypt(token).decode()
