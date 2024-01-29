import matplotlib.pyplot as plt

class CustomVisualization:
    def __init__(self):
        self.device_transmissions = []
        self.queue_lengths = []
        self.all_transmission_times = []

    def record_device_transmission(self, device_id, time):
        self.device_transmissions.append((device_id, time))

    def record_queue_length(self, queue_length, time):
        self.queue_lengths.append((queue_length, time))

    def record_all_transmission_times(self, time):
        self.all_transmission_times.append(time)

    def plot_average_delay(self):
        if not self.device_transmissions:
            print("No device transmissions recorded.")
            return

        device_ids, device_times = zip(*self.device_transmissions)

        # Фильтруем события по времени
        device_ids = [device_id for device_id, time in zip(device_ids, device_times)]
        device_times = [time for time in device_times]

        if not device_ids:
            print("No device transmissions recorded.")
            return

        # Вычисляем среднюю задержку
        delays = [device_times[i] - device_times[i - 1] for i in range(1, len(device_times))]

        # Строим график средней задержки
        plt.plot(device_times[1:], delays, label='Average Delay')
        plt.xlabel('Time')
        plt.ylabel('Average Delay')
        plt.legend()
        plt.show()

    def plot_queue_length(self):
        if not self.queue_lengths:
            print("No queue lengths recorded.")
            return

        queue_lengths, queue_times = zip(*self.queue_lengths)

        # Строим график количества сообщений в очереди
        plt.plot(queue_times, queue_lengths, label='Queue Length')
        plt.xlabel('Time')
        plt.ylabel('Queue Length')
        plt.legend()
        plt.show()

    def plot_all_transmission_times(self):
        if not self.all_transmission_times:
            print("No transmission times recorded.")
            return

        # Строим график времени всех передач данных
        plt.plot(self.all_transmission_times, range(1, len(self.all_transmission_times) + 1), label='Transmission Times')
        plt.xlabel('Time')
        plt.ylabel('Transmission Times')
        plt.legend()
        plt.show()