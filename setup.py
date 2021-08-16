import getpass
import json
from datetime import datetime


def ask(question, possible_answers=False):
    while True:
        answer = input(question)

        if possible_answers:
            if answer in possible_answers:
                return answer
            else:
                print(
                    f"Whoops! Wrong answer, the only possible answers are: {', '.join(possible_answers)}."
                )
        else:
            return answer


def ask_date(question, format):
    while True:
        answer = input(question)

        try:
            datetime.strptime(answer, format)
            return answer
        except Exception as e:
            print(e)
            print(f"Whoops! Wrong answer, the correct date format is '{format}'.")


def ask_int(question):
    while True:
        answer = input(question)

        try:
            answer = int(answer)
            return answer
        except Exception:
            print(f"Whoops! Wrong answer, the valid answer is an integer.")


if __name__ == "__main__":
    current_os = ask(
        "Hey there! What OS are you on? [linux/mac, EX: 'linux'] ",
        ["linux", "mac"],
    )
    username = ask("What is your BU login username? ")
    password = getpass.getpass("What is your BU login password? (won't display) ")

    want_tests = ask(
        "Do you want the bot to schedule tests for you? [yes,no] ", ["yes", "no"]
    )
    display = ask(
        "What is your current display value? (run 'env | grep -e \"DISPLAY\"')[':N',EX:':1'] "
    )
    last_bot_run = "1/1/2000"

    if want_tests == "yes":
        os_user = ask("What is your current user? (run 'id -un') ")
        last_test = ask_date(
            "When was your last test? (month/day/year, EX: '8/14/2021') ", "%m/%d/%Y"
        )
        tests_every = ask_int(
            "How often do you want your tests to be scheduled? (in days, EX: '7') "
        )
        test_loc = ask(
            "What is your preferred testing site? [808/Aganis/BUMC-72] ",
            ["808", "Aganis", "BUMC-72"],
        )
        test_time = ask_date(
            "What is your preferred testing time? [HH:MM AM/PM, EX:'9:30 AM' ] ",
            "%I:%M %p",
        )
        book_ahead = ask_int(
            "How many days before your test do you want to schedule it? [Max: 6, EX:'6' ] "
        )

        config = {
            "current_os": current_os,
            "username": username,
            "password": password,
            "want_tests": want_tests,
            "display": display,
            "os_user": os_user,
            "last_test": last_test,
            "tests_every": tests_every,
            "test_loc": test_loc,
            "test_time": test_time,
            "book_ahead": book_ahead,
            "last_bot_run": last_bot_run,
        }
    else:
        config = {
            "current_os": current_os,
            "username": username,
            "password": password,
            "want_tests": want_tests,
            "display": display,
            "last_bot_run": last_bot_run,
        }

    print("Great! Everything is set up. Now run: python main.py")

    with open("config.json", "w") as file:
        json.dump(config, file)
