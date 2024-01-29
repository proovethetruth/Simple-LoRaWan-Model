
import simpy
from random import uniform

from channel import Channel
from device import Device
from gateway import Gateway
from visualization import Visualization

time_of_modeling = int(input())

# Создаем среду SimPy
env = simpy.Environment()

# Создаем объект визуализации
visualization = Visualization()

# Создаем объекты канала, шлюза и устройств
channel = Channel(env)
gateway = Gateway(env, visualization)  # Передаем объект visualization в Gateway
devices = [Device(env, device_id, channel, gateway, visualization) for device_id in range(1, 6)]

# Передача данных от устройств
for device in devices:
    env.process(device.transmit_data())  # Мы больше не передаем интервал, поскольку он установлен по умолчанию в функции

# Запускаем среду SimPy
env.run(until=time_of_modeling)  # Увеличиваем время моделирования до 20 единиц времени

# В конце моделирования вызываем метод для отображения графика
visualization.plot_events(max_time=time_of_modeling)
