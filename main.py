
import simpy
from random import uniform

from channel import Channel
from device import Device
from gateway import Gateway
from visualization import CustomVisualization

time_of_modeling = int(input())
env = simpy.Environment()

visualization = CustomVisualization()
channel = Channel(env, 10)
gateway = Gateway(env)
devices = [Device(env, device_id, channel, gateway, visualization) for device_id in range(1, 5)]


for device in devices:
    env.process(device.transmit_data())

env.run(until=time_of_modeling)

print(f"Total number of messages recieved: {gateway.get_num_messages_sent()}")
print("Total number of attempts:", sum(device.print_attempts() for device in devices))

visualization.plot_waiting_messages()