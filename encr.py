import os
from cryptography.fernet import Fernet

def get_path_key() -> str:
    # Obtener la ruta donde se guardará la clave
    current_dir = os.path.dirname(os.path.abspath(__file__))
    keys_dir = os.path.join(current_dir, 'keys')  # Modificado para crear la carpeta en el mismo directorio
    if not os.path.exists(keys_dir):
        os.makedirs(keys_dir)  # Crear el directorio si no existe
    aes_key_path = os.path.join(keys_dir, 'aes_key.key')
    return aes_key_path

def generate_key() -> None:
    # Generar y guardar la clave
    key = Fernet.generate_key()
    with open(get_path_key(), 'wb') as key_file:
        key_file.write(key)

class AESEncrypt:

    @staticmethod
    def load_key(path: str) -> bytes:
        # Cargar la clave desde el archivo
        with open(path, 'rb') as key_file:
            return key_file.read()

    def __init__(self) -> None:
        # Cargar la clave y crear un objeto Fernet
        if not os.path.exists(get_path_key()):
            generate_key()  # Generar una nueva clave si no existe
        self.key = self.load_key(get_path_key())
        self.fernet = Fernet(self.key)

    def encrypt(self, message: str) -> bytes:
        # Encriptar el mensaje
        return self.fernet.encrypt(message.encode())

    def decrypt(self, token: bytes) -> str:
        # Desencriptar el mensaje
        return self.fernet.decrypt(token).decode()

# Inicializar la clase de encriptación
aes_encrypt = AESEncrypt()

# Mensaje original
mensaje_original = "huevos"

# Encriptar el mensaje
mensaje_encriptado = aes_encrypt.encrypt(mensaje_original)
print("Mensaje encriptado:", mensaje_encriptado)

# Desencriptar el mensaje
try:
    mensaje_desencriptado = aes_encrypt.decrypt(mensaje_encriptado)
    print("Mensaje desencriptado:", mensaje_desencriptado)
except Exception as e:
    print("Error al desencriptar el mensaje:", str(e))
