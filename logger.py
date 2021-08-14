import os
from datetime import datetime

current_path = os.path.dirname(os.path.realpath(__file__))
logs_file = os.path.join(current_path, "logs/bot.log")


class Logger:
    def __init__(self):
        return

    def error(self, msg):
        now = datetime.today().strftime("%m/%d/%Y %H:%M:%S")
        self.write(f"{now} -- Error: {msg}")

    def log(self, msg):
        now = datetime.today().strftime("%m/%d/%Y %H:%M:%S")
        self.write(f"{now} -- Output: {msg}")

    def write(self, msg):
        logs = open(logs_file, "a")
        logs.write(msg + "\n")
        logs.close()
