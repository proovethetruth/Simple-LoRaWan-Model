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
        self.visualization = visualization
        self.key = self.generate_key()  # Генерация ключа для каждого устройства
        self.transmission_interval = self.generate_transmission_interval()

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
            # Немедленно передаем данные после пробуждения
            print(f"Device {self.id} transmitting data at time {self.env.now}")

            # Формирование кадра
            plaintext_payload = lorem.words(3)
            encrypted_payload = self.encrypt_payload(plaintext_payload)
            frame = Frame(device_id=self.id, payload=encrypted_payload)

            # Передача кадра
            self.env.process(self.transmit_frame(frame))

            # Ожидаем интервал перед следующей передачей
            yield self.env.timeout(self.transmission_interval)

    def transmit_frame(self, frame):
            channel_index = self.channel.request_channel()
            if channel_index is not None:
                transmission_time = self.env.now
                yield self.env.timeout(randint(1, 5))
                self.gateway.process_frame(frame, channel_index)
                self.channel.release_channel(channel_index)
                
                # Добавим запись статистики визуализации о длине очереди
                self.visualization.record_queue_length(len(self.env._queue), self.env.now)
                # Добавим запись статистики визуализации о времени передачи данных
                self.visualization.record_all_transmission_times(transmission_time)
        
    def generate_transmission_interval(self):
        return randint(2, 8)