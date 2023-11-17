class qa:
    COLORS = {
        'yellow': '\033[93m',
        'green': '\033[92m',
        'blue': '\033[94m',
        'red': '\033[91m'
    }

    def __init__(self, text, color='yellow'):
        color_code = self.COLORS.get(color, self.COLORS['yellow'])  # default to yellow
        print(color_code + text + '\033[0m')  # \033[0m resets the color