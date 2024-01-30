from random import uniform, randint
from lorem_text import lorem
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import simpy

from frame import Frame

class Device:
    def __init__(self, env, id, channel, gateway, visualization):
        self.env = env
        self.id = id
        self.channel = channel
        self.gateway = gateway
        self.key = self.generate_key()  # Генерация ключа для каждого устройства
        self.transmission_interval = self.generate_transmission_interval()
        self.failed_transmission_attempts = 0
        self.visualization = visualization

    def generate_key(self):
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
            # Слушаем канал перед передачей
            while True:
                self.failed_transmission_attempts += 1
                print(f"Device {self.id} waiting for a channel...")
                self.visualization.record_waiting_messages(self.failed_transmission_attempts, self.env.now)  # Записываем количество ожидающих сообщений
                channel_index = self.channel.request_channel()
                if channel_index is not None:
                    break
                else:
                    yield self.env.timeout(1)

            # Производим передачу данных
            print(f"Device {self.id} transmitting data at time {self.env.now} on channel {channel_index}")
            self.failed_transmission_attempts -= 1
            # Формирование кадра
            plaintext_payload = lorem.words(3)
            encrypted_payload = self.encrypt_payload(plaintext_payload)
            frame = Frame(device_id=self.id, payload=encrypted_payload)

            # Передача кадра
            self.env.process(self.transmit_frame(frame, channel_index))

            # Освобождаем канал
            yield self.env.timeout(0)  # Используем нулевой таймаут, чтобы убедиться, что освобождение происходит сразу
            self.channel.release_channel(channel_index)

            # Ожидаем интервал перед следующей передачей
            yield self.env.timeout(self.transmission_interval)


    def transmit_frame(self, frame, channel_index):
        yield self.env.timeout(randint(1, 5))
        self.gateway.process_frame(frame, channel_index)

    def generate_transmission_interval(self):
        return randint(2, 8)
    
    def print_attempts(self):
        return self.failed_transmission_attempts