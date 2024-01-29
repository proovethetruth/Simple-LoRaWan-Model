
class Channel:
    def __init__(self, env, num_channels=1):
        self.env = env
        self.available_channels = [True] * num_channels

    def request_channel(self):
        for i, available in enumerate(self.available_channels):
            if available:
                self.available_channels[i] = False
                return i
        return None

    def release_channel(self, channel_index):
        self.available_channels[channel_index] = True
