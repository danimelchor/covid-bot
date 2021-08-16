import getpass
import json

if __name__ == "__main__":
    config = {
        "current_os": input("Hey there! What OS are you on? [linux/mac, EX: 'linux'] "),
        "os_user": input("What is your current user? (run 'id -un') "),
        "username": input("What is your BU login username? "),
        "password": getpass.getpass("What is your BU login password? (won't display) "),
        "last_test": input(
            "When was your last test? (month/day/year, EX: '8/14/2021') "
        ),
        "tests_every": int(
            input(
                "How often do you want your tests to be scheduled? (in days, EX: '7') "
            )
        ),
        "test_loc": input("What is your preferred testing site? [808/Aganis/BUMC-72] "),
        "test_time": input(
            "What is your preferred testing time? [HH:MM AM/PM, EX:'9:30AM' ] "
        ).replace(" ", ""),
        "book_ahead": int(
            input(
                "How many days before your test do you want to schedule it? [Max: 6, EX:'6' ] "
            )
        ),
        "display": input(
            "What is your current display value? (run 'env | grep -e \"DISPLAY\"')[':N',EX:':1'] "
        ),
        "last_bot_run": "1/1/2000",
    }

    print("Great! Everything is set up. Now run: python main.py")

    with open("config.json", "w") as file:
        json.dump(config, file)
