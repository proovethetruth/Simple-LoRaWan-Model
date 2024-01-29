
from random import uniform, randint
from lorem_text import lorem
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

from frame import Frame


class Device:
    def __init__(self, env, id, channel, gateway, visualization):
        self.env = env
        self.id = id
        self.channel = channel
        self.gateway = gateway
        self.key = self.generate_key()  # Генерация ключа для каждого устройства
        self.visualization = visualization
        self.transmission_interval = self.generate_transmission_interval()

    def check_channel_availability(self):
        return self.channel.available

    def generate_key(self):
        # В реальном применении ключи должны быть управляемыми и безопасными, это просто для демонстрации
        return b'\x01' * 16  # Используем статический ключ для примера

    def encrypt_payload(self, payload):
        # Используем режим CBC с дополнением PKCS7
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(bytes([0] * 16)), backend=default_backend())
        encryptor = cipher.encryptor()

        # Дополняем данные
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(payload.encode('utf-8')) + padder.finalize()

        # Шифруем данные
        return encryptor.update(padded_data) + encryptor.finalize()

    def transmit_data(self):
        while True:
            interval = self.transmission_interval
            yield self.env.timeout(interval)

            if self.check_channel_availability():
                self.channel.available = False  # Занимаем канал

                # Формирование кадра
                plaintext_payload = lorem.words(3)  # Генерация трех слов в стиле Lorem Ipsum
                encrypted_payload = self.encrypt_payload(plaintext_payload)
                frame = Frame(device_id=self.id, payload=encrypted_payload)

                # Передача кадра
                print(f"Device {self.id} transmitting data at time {self.env.now}")
                self.env.process(self.transmit_frame(frame))  # Асинхронный вызов передачи кадра

            self.channel.available = True  # Освобождаем канал
            self.visualization.record_device_transmission(self.id, self.env.now)


    def transmit_frame(self, frame):
        yield self.env.timeout(randint(1, 5))
        self.gateway.process_frame(frame)
        self.channel.available = True
        
    def generate_transmission_interval(self):
        return 2
