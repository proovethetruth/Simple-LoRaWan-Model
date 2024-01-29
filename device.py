from random import uniform, randint
from lorem_text import lorem
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

from frame import Frame

class Device:
    def __init__(self, env, id, channel, gateway, visualization, transmission_mode='LoRaWan'):
        self.env = env
        self.id = id
        self.channel = channel
        self.gateway = gateway
        self.visualization = visualization
        self.key = self.generate_key()
        self.transmission_interval = self.generate_transmission_interval()
        self.transmission_mode = transmission_mode
        self.transmission_attempts = 0  # Добавим счетчик попыток передачи
        self.lost_packets = 0  # Добавим счетчик потерянных пакетов


    def check_channel_availability(self):
        return self.channel.available

    def generate_key(self):
        return b'\x01' * 16  # Используем статический ключ для примера

    def encrypt_payload(self, payload):
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(bytes([0] * 16)), backend=default_backend())
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(payload.encode('utf-8')) + padder.finalize()
        return encryptor.update(padded_data) + encryptor.finalize()

    def transmit_data(self):
        while True:
            print(f"Device {self.id} transmitting data at time {self.env.now}")

            if self.transmission_mode == 'L':
                self.transmit_data_lorawan()
            elif self.transmission_mode == 'A':
                self.transmit_data_aloha()
            else:
                raise ValueError("Invalid transmission mode. Use 'L' or 'A'.")

            interval = self.transmission_interval
            yield self.env.timeout(interval)

    def transmit_data_lorawan(self):
        if self.check_channel_availability():
            self.channel.available = False
            plaintext_payload = lorem.words(3)
            encrypted_payload = self.encrypt_payload(plaintext_payload)
            frame = Frame(device_id=self.id, payload=encrypted_payload)
            self.env.process(self.transmit_frame(frame))
        else:
            self.channel.available = True
            self.visualization.record_device_transmission(self.id, self.env.now)

    def transmit_data_aloha(self):
        # Просто пытаемся передать в ALOHA, не учитывая доступность канала
        plaintext_payload = lorem.words(3)
        encrypted_payload = self.encrypt_payload(plaintext_payload)
        frame = Frame(device_id=self.id, payload=encrypted_payload)
        self.env.process(self.transmit_frame(frame))

    def transmit_frame(self, frame):
            self.transmission_attempts += 1  # Увеличиваем счетчик попыток передачи
            transmission_time = self.env.now
            yield self.env.timeout(randint(1, 5))

            if self.check_channel_availability():
                self.gateway.process_frame(frame)
                self.channel.available = True
                self.visualization.record_all_transmission_times(transmission_time)
            else:
                self.visualization.record_queue_length(self.transmission_attempts, self.env.now)
                self.lost_packets += 1  # Увеличиваем счетчик потерянных пакетов

    def print_lost_packets(self):
        print(f"Total lost packets: {self.lost_packets}")

    def generate_transmission_interval(self):
        return randint(2, 8)
