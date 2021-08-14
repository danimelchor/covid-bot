# Boston University symptom survey and covid-19 appointment maker
# By Daniel Melchor (Class of 2024)
# Inspired by Nic Nguyen

import argparse
import json
import os
from datetime import date, datetime

from crontab import CronTab

from bot import Bot
from logger import Logger

# Logger to check output from CRON
logger = Logger()

# Absolute paths for CRON
current_path = os.path.dirname(os.path.realpath(__file__))
config_file = os.path.join(current_path, "config.json")

# Load and parse config
try:
    with open(config_file, "r") as file:
        config = json.load(file)
        file.close()

    OS = config["current_os"].lower()
    USERNAME = config["username"]
    OS_USER = config["os_user"]
    PASSWORD = config["password"]
    TESTS_EVERY = int(config["tests_every"])
    LAST_TEST = datetime.strptime(config["last_test"], "%m/%d/%Y")
    TEST_LOC = config["test_loc"]
    TEST_TIME = datetime.strptime(config["test_time"], "%I:%M%p")
    BOOK_AHEAD_DAYS = int(config["book_ahead"])
    DISPLAY = config["display"]
    LAST_BOT_RUN = datetime.strptime(config["last_bot_run"], "%m/%d/%Y")
except Exception as e:
    print("Please complete the setup with the command: python setup.py")
    print(f"Error: {e}")
    exit()


def schedule_cron():
    """
    Schedule a CRON job with a target of this bot
    """
    my_cron = CronTab(user=OS_USER)
    current_dir = os.path.dirname(os.path.realpath(__file__))

    # Run from VENV if any
    try:
        venv_path = os.environ["VIRTUAL_ENV"] + "/bin/python"
        boot_job = my_cron.new(
            command=f"{venv_path} {current_dir}/main.py --cron", comment="covid-bot"
        )
    except Exception:
        boot_job = my_cron.new(
            command=f"python {current_dir}/main.py --cron", comment="covid-bot"
        )

    # Job on boot
    boot_job.env["DISPLAY"] = DISPLAY
    boot_job.every_reboot()

    # Save changes
    my_cron.write()
    print(
        "Cron job scheduled successfully - your surveys will be completed every time you open your computer for the first time that day."
    )
    print("If you wish to delete it run 'python main.py --delete'")


def delete_cron():
    """
    Delete the existing CRON jobs with a target of this bot
    """
    my_cron = CronTab(user=OS_USER)
    my_cron.remove_all(comment="covid-bot")
    my_cron.write()
    print("Cron job deleted successfully")


def run_bot(hidden):
    """
    Run bot with or without an interface if its the first time that day
    """
    if (datetime.today() - LAST_BOT_RUN).days > 0:
        try:
            # Logging
            logger.log("Started Bot From Cron")

            # Start run
            bot = Bot(
                OS,
                hidden,
                USERNAME,
                PASSWORD,
                TESTS_EVERY,
                LAST_TEST,
                TEST_LOC,
                TEST_TIME,
                BOOK_AHEAD_DAYS,
            )
            bot.start()

            # Logging
            logger.log("Successfully finished execution from cron")

            # Save successful execution date to now
            file = open(config_file, "r")
            config = json.load(file)
            file.close()
            config["last_bot_run"] = datetime.now().strftime("%m/%d/%Y")
            file = open(config_file, "w")
            json.dump(config, file)
            file.close()
        except Exception as e:
            print(
                "Oh no! There was an error. Make sure your setup (from setup.py) was correct (you can check it inside config.json). If its, please email dmelchor@bu.edu so I can fix it. Sorry!"
            )
            print(f"Error: {e}")
            logger.error(e)


def get_args():
    """
    Load arguments from cmd
    """
    parser = argparse.ArgumentParser(
        description="Autocomplete BU's survey and schedule tests."
    )
    parser.add_argument("--run", help="run the bot now.", action="store_true")
    parser.add_argument(
        "--schedule",
        help="schedule a cron job for the bot to run every day.",
        action="store_true",
    )
    parser.add_argument(
        "--delete",
        help="delete the cron job scheduled for this file.",
        action="store_true",
    )
    parser.add_argument(
        "--cron",
        help="the option called from cron to hide the interface.",
        action="store_true",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()

    # If no argument, ask the user
    if not args.run and not args.schedule and not args.delete and not args.cron:
        option = input(
            "Do you want to run the bot visually, schedule its execution for every day, or delete the scheduled execution? [run/schedule/delete] "
        )
    else:
        option = (
            "run"
            if args.run
            else "schedule"
            if args.schedule
            else "delete"
            if args.delete
            else "cron"
        )

    # Depending on the args we run a different function/method
    if option == "run":
        run_bot(hidden=False)
    elif option == "cron":
        run_bot(hidden=True)
    elif option == "schedule":
        schedule_cron()
    elif option == "delete":
        delete_cron()
    else:
        print("Whoops! The only options are 'schedule', 'delete' and 'run'")
