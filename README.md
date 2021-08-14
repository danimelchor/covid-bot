# Boston University COVID-19 Bot

## Requirements

This bot uses cron jobs to schedule the execution every day. Therefore, only computers using UNIX based systems (mac/linux) can use it. Windows will probably be implemented in the future.

## Setup

This bot is created with python. First, you will need to have python installed (which usually comes by default). To check if you have it run:

```bash
python -V
```

Then, you will also need python's package installer [pip](https://pypi.org/project/pip/) (which also usually comes by default). To check if you have it run:

```bash
pip -V
```

Then, to install its dependencies run

```
pip install -r requirements.txt
```

_Note: you may want to user a [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) for the installed packages_

## Configuration

### Before you begin

Before you begin you need to find out what your current user is with

```bash
id -un
```

You will also need to find out what your display configuration is, for this run

```bash
env | grep -e "DISPLAY"
```

_Note: the answer to these two questions is everything after the = sign_

### Setup

The bot uses the configuration found in `config.json`. To first create this file run:

```bash
python setup.py
```

and answer all the questions.

## Usage

To start using the bot, you will need to run:

```bash
python main.py --run
```

## Scheduling the bot

Since surveys need to be completed every day, and tests every week, it is convenient if you schedule the python bot and let it run every day by itself.

To schedule the bot run:

```
python main.py --schedule
```

This will create a [cron job](https://en.wikipedia.org/wiki/Cron) that will run once a day (if you start your computer at least once that day).

To check if it created anything after running that command, type

```bash
crontab -l
```

---

###### By Daniel Melchor (Class of 2024)

###### Heavily inspired by [Nic Nguyen](https://github.com/nico22nguyen)
