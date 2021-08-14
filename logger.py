import os
from datetime import datetime

current_path = os.path.dirname(os.path.realpath(__file__))
logs_file = os.path.join(current_path, "logs/bot.log")


class Logger:
    """
    A simple class for saving log messages and errors to logs/bot.log
    """

    def __init__(self):
        return

    def error(self, msg):
        """
        Saves an error with message msg to the logs
        """
        now = datetime.today().strftime("%m/%d/%Y %H:%M:%S")
        self.write(f"{now} -- Error: {msg}")

    def log(self, msg):
        """
        Saves an log with message msg to the logs
        """
        now = datetime.today().strftime("%m/%d/%Y %H:%M:%S")
        self.write(f"{now} -- Output: {msg}")

    def write(self, msg):
        """
        Writes the file with whatever message msg is passed in
        """
        logs = open(logs_file, "a")
        logs.write(msg + "\n")
        logs.close()
