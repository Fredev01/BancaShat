import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)


def get_path_key(name_key: str) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    keys_dir = os.path.join(current_dir, '..', 'keys')
    aes_key_path = os.path.join(keys_dir, name_key)
    return aes_key_path


def save_private_key_on_file() -> None:
    path = get_path_key('private_key.pem')
    with open(path, 'wb') as priv_file:
        priv_file.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
        )


def save_public_key_on_file() -> None:
    path = get_path_key('public_key.pem')
    public_key = private_key.public_key()
    with open(path, 'wb') as pub_file:
        pub_file.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )


class RSAEncrypt:
    @staticmethod
    def load_private_key(path: str):
        with open(path, 'rb') as key_file:
            return serialization.load_pem_private_key(key_file.read(), password=None)

    @staticmethod
    def load_public_key(path: str):
        with open(path, 'rb') as key_file:
            return serialization.load_pem_public_key(key_file.read())

    def __init__(self) -> None:
        self.private_key = self.load_private_key(get_path_key('private_key.pem'))
        self.public_key = self.load_public_key(get_path_key('public_key.pem'))

    def encrypt(self, message: str) -> bytes:
        return self.public_key.encrypt(
            message.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    def decrypt(self, token: bytes) -> str:
        token_bytes = self.private_key.decrypt(
            token,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return token_bytes.decode('utf-8')


if __name__ == '__main__':
    # no need to run this file
    save_private_key_on_file()
    save_public_key_on_file()