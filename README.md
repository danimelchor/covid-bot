![version](https://img.shields.io/badge/version-2.0.1-blue)
![license](https://img.shields.io/badge/license-MIT-green)

# **Boston University COVID-19 Bot**

## **Requirements**

This bot uses cron jobs to schedule the execution every day. Therefore, only computers using UNIX based systems (mac/linux) can use it. Windows will probably be implemented in the future.

Also, this bot uses a framework called [selenium](https://selenium-python.readthedocs.io/). Therefore, it requires what is called a "chromedriver" executable. The ones included with the repository are for chrome version 92. If you have a different chrome version, please download it from [here](https://chromedriver.chromium.org/downloads) and save it with the name `<YOUR-OS-HERE>_chromedriver` like the ones in the folder `drivers/`.

To check your version of chrome, open chrome and click on the 3 dots on the top right, then click settings. All the way at the bottom there should be an "About Chrome" link. There you will be able to find your current Chrome version with the format `9X.X.X.X` where we are only interested in the first two numbers. If your version is not 92, please download your version of chromedriver.

## **Setup**

This bot is created with python. First, you will need to have python installed (which usually comes by default). To check if you have it run:

```bash
python -V
```

Then, you will also need python's package installer [pip](https://pypi.org/project/pip/) (which also usually comes by default). To check if you have it run:

```bash
pip -V
```

Then, to install its dependencies run

```bash
pip install -r requirements.txt
```

_Note: you may want to user a [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) for the installed packages_

## **Configuration**

### Before you begin

Before you begin you need to find out what your current user is. Find it by typing in your cmd line

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

## **Usage**

To start using the bot, you will need to run:

```bash
python main.py --run
```

## **Scheduling the bot**

Since surveys need to be completed every day, and tests every week, it is convenient if you schedule the python bot and let it run every day by itself.

To schedule the bot run:

```bash
python main.py --schedule
```

This will create a [cron job](https://en.wikipedia.org/wiki/Cron) that will run once a day (if you start your computer at least once that day).

To check if it created anything after running that command, type

```bash
crontab -l
```

## **Contributions**

I am open to any type of contribution/suggestion. Just open a pull request directly to master and I will review your code and merge it. Please make sure your code is well formatted using [black](https://github.com/psf/black).

## **Terms of usage**

I have made it as a project to make the process of completing your survey easier, but you are responsible for providing true information to BU's patient connect platform. If you do have any symptoms you are also responsible for telling to BU since, if the bot is running, it will say you don't have any symptoms. Please make sure you comply with BU PatientConnect's terms of usage and don't use the bot for any malicious actions. I am in no way responsible for your actions with this code.

## **Future Improvements**

Since I have not been able to reproduce the error patient connect gives when it thinks a slot is opened, but it is actually full (once you click it there is a red text saying that there was an error and that it is full), this error is not accounted for. If you get it, it is probably a good idea to force a re-run using the `python main.py --run` command.

I will also try to implement the Windows possibility once I understand how the task scheduler works.

---

###### By [Daniel Melchor](https://danielmelchor.com) (Class of 2024)

###### Heavily inspired by [Nic Nguyen](https://github.com/nico22nguyen)
