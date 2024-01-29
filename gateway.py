
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding


class Gateway:
    def __init__(self, env):
        self.env = env

    def decrypt_payload(self, encrypted_payload, device_key):
        # Используем режим CBC с дополнением PKCS7
        cipher = Cipher(algorithms.AES(device_key), modes.CBC(bytes([0] * 16)), backend=default_backend())
        decryptor = cipher.decryptor()

        # Дешифруем данные
        decrypted_data = decryptor.update(encrypted_payload) + decryptor.finalize()

        # Удаляем дополнение
        unpadder = padding.PKCS7(128).unpadder()
        return unpadder.update(decrypted_data) + unpadder.finalize()

    def process_frame(self, frame):
        # Логика обработки кадра
        decrypted_payload = self.decrypt_payload(frame.payload, device_key=b'\x01' * 16)
        print(f"Gateway received frame from Device {frame.device_id} with decrypted payload: {decrypted_payload.decode('utf-8')}\n")
