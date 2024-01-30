import matplotlib.pyplot as plt

class CustomVisualization:
    def __init__(self):
        self.waiting_messages = []

    def record_waiting_messages(self, num_messages, time):
        self.waiting_messages.append((num_messages-1, time))

    def plot_waiting_messages(self):
        if not self.waiting_messages:
            print("No waiting messages recorded.")
            return

        num_messages, times = zip(*self.waiting_messages)

        # Строим график количества ожидающих сообщений (красный цвет) с прямыми углами
        plt.step(times, num_messages, label='Waiting Messages', color='red', where='post')
        plt.xlabel('Time')
        plt.ylabel('Number of Waiting Messages')

        # Настройка отображения осей Y без отрицательных значений
        plt.ylim(bottom=0)
        plt.xticks(range(int(min(times)), int(max(times)) + 1, 1))

        plt.legend()
        plt.show()