import matplotlib.pyplot as plt


class Visualization:
    def __init__(self):
        self.device_transmissions = []
        self.gateway_receptions = []
        self.forced_delays = []  # Добавим список для отслеживания вынужденных задержек

    def record_device_transmission(self, device_id, time):
        self.device_transmissions.append((device_id, time))

    def record_gateway_reception(self, device_id, time, forced_delay=None):
        self.gateway_receptions.append((device_id, time))
        if forced_delay is not None:
            self.forced_delays.append((device_id, time, forced_delay))

    def plot_events(self, max_time):
        if not self.device_transmissions:
            print("No device transmissions recorded.")
            return

        device_ids, device_times = zip(*self.device_transmissions)
        gateway_ids, gateway_times = zip(*self.gateway_receptions)

        if self.forced_delays:
            forced_delay_ids, forced_delay_times, forced_delays = zip(*self.forced_delays)
        else:
            forced_delay_ids, forced_delay_times, forced_delays = [], [], []

        # Фильтруем события по времени
        device_ids = [device_id for device_id, time in zip(device_ids, device_times) if time <= max_time]
        device_times = [time for time in device_times if time <= max_time]
        gateway_ids = [gateway_id for gateway_id, time in zip(gateway_ids, gateway_times) if time <= max_time]
        gateway_times = [time for time in gateway_times if time <= max_time]

        print("Filtered device transmissions:", list(zip(device_ids, device_times)))
        print("Filtered gateway receptions:", list(zip(gateway_ids, gateway_times)))

        if not device_ids:
            print("No device transmissions recorded within the specified time.")
            return

        # Используем целочисленные значения для Device ID
        plt.scatter(device_times, device_ids, c='blue', marker='o', label='Device Transmission')
        plt.scatter(gateway_times, gateway_ids, c='red', marker='x', label='Gateway Reception')

        # Отмечаем вынужденные задержки
        for forced_delay_time, forced_delay_id, forced_delay in zip(forced_delay_times, forced_delay_ids, forced_delays):
            plt.annotate(
                f'Forced Delay: {forced_delay}',
                xy=(forced_delay_time, forced_delay_id),
                xytext=(forced_delay_time, forced_delay_id + 0.2),
                arrowprops=dict(facecolor='black', arrowstyle='->')
            )

        plt.xlabel('Time')
        plt.ylabel('Device ID')
        plt.legend()
        plt.yticks(range(1, max(device_ids) + 1))  # Используем целочисленные значения для Device ID
        plt.show()
