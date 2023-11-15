
import simpy, random

from channel import Channel
from device import Device
from gateway import Gateway
from frame import Frame

if __name__ == "__main__":
    # Создание среды моделирования
    env = simpy.Environment()

    # Создание канала, узлов и шлюза
    channel = Channel(env)
    gateway = Gateway(env, channel=channel)
    nodes = [Device(env, id=i, channel=channel, gateway=gateway) for i in range(1, 21)]  # Создаем 20 узлов

    # Запуск процессов передачи данных от разных узлов к шлюзу
    for node in nodes:
        env.process(node.transmit_data(interval=random.randint(1, 5)))  # Используем случайные интервалы

    # Запуск среды моделирования
    env.run(until=50)  # Увеличиваем время моделирования до 50 единиц времени
