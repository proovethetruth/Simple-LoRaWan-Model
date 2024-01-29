
import simpy
from random import uniform

from channel import Channel
from device import Device
from gateway import Gateway
from visualization import CustomVisualization

time_of_modeling = int(input())
env = simpy.Environment()

# Создаем объект визуализации
custom_visualization = CustomVisualization()

channel = Channel(env, num_channels=1)  # Здесь 3 - количество каналов
gateway = Gateway(env)
devices = [Device(env, device_id, channel, gateway, custom_visualization) for device_id in range(1, 6)]


for device in devices:
    env.process(device.transmit_data())

env.run(until=time_of_modeling)

# В конце моделирования вызываем методы для отображения графиков
custom_visualization.plot_queue_length()
print(f"Total number of messages sent: {gateway.get_num_messages_sent()}")