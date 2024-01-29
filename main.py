
import simpy
from random import uniform

from channel import Channel
from device import Device
from gateway import Gateway
from visualization import CustomVisualization

print("Enter time of modeling: ")
time_of_modeling = int(input())

print("LoRaWan / ALOHA (L/A): ")
mode = str(input())

env = simpy.Environment()

# Создаем объект визуализации
custom_visualization = CustomVisualization()

channel = Channel(env)
gateway = Gateway(env)
devices = [Device(env, device_id, channel, gateway, custom_visualization, mode) for device_id in range(1, 6)]

for device in devices:
    env.process(device.transmit_data())

env.run(until=time_of_modeling)

for device in devices:
    device.print_lost_packets()

# В конце моделирования вызываем методы для отображения графиков
custom_visualization.plot_queue_length()
custom_visualization.print_total_messages_transmitted()