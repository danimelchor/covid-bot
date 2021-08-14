import os
import time
from datetime import date, datetime, timedelta

# Import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from logger import Logger

logger = Logger()

# Absolute paths for CRON
current_path = os.path.dirname(os.path.realpath(__file__))


class Bot:
    def __init__(
        self,
        current_os,
        hidden,
        username,
        password,
        tests_every,
        last_test,
        test_loc,
        test_time,
        book_ahead,
    ):
        self.current_os = current_os
        self.hidden = hidden
        self.username = username
        self.password = password
        self.tests_every = tests_every
        self.last_test = last_test
        self.test_loc = test_loc
        self.test_time = test_time
        self.book_ahead = book_ahead

    def start(self):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-setuid-sandbox")
        if self.hidden:
            options.add_argument("--headless")

        # Location of your chrome driver
        DRIVER_PATH = f"drivers/{self.current_os}_chromedriver"
        DRIVER_PATH = os.path.join(current_path, DRIVER_PATH)

        # Initiate chrome and wait for load
        driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)
        driver.implicitly_wait(15)
        driver.set_page_load_timeout(15)

        # Go to patientconnect homepage for symptom survey
        driver.get("https://patientconnect.bu.edu")

        self.driver = driver
        self.login()

    def login(self):
        login_username = self.driver.find_element_by_xpath('//*[@id="j_username"]')
        login_username.send_keys(self.username)

        login_password = self.driver.find_element_by_xpath('//*[@id="j_password"]')
        login_password.send_keys(self.password)

        self.driver.find_element_by_xpath('//*[@id="wrapper"]/div/form/button').click()
        logger.log("User logged in")

        self.complete_survey()
        logger.log("Survey completed")

        self.schedule_test()
        self.driver.close()

    def complete_survey(self):
        self.driver.find_element_by_xpath(
            '//a[contains(text(),"Complete Survey")]'
        ).click()
        self.driver.find_element_by_xpath('//a[contains(text(),"Continue")]').click()
        self.driver.find_element_by_xpath('//label[contains(text(),"No")]').click()
        self.driver.find_element_by_xpath('//input[@value = "Continue"]').click()

    def schedule_test(self):
        today = datetime.today()
        delta = today - self.last_test

        if abs(delta.days) % self.tests_every != self.tests_every - self.book_ahead:
            return

        self.driver.get("https://patientconnect.bu.edu/appointments_home.aspx")
        self.driver.find_element_by_xpath(
            '//input[@value = "Schedule an Appointment"]'
        ).click()

        # All checkboxes
        ids = [297, 496, 493, 484, 478, 498]
        for id in ids:
            self.driver.find_element_by_xpath(f'//*[@id="{id}"]').click()
            self.driver.find_element_by_xpath('//*[@id="cmdProceed"]').click()

        # Confirm contact info
        self.driver.find_element_by_xpath('//*[@id="cmdStandardProceed"]').click()

        # Select test date
        test_date = date.today() + timedelta(self.book_ahead)
        test_data_to_txt = test_date.strftime("%m/%d/%Y")

        self.driver.find_element_by_xpath('//*[@id="StartDate"]').send_keys(
            Keys.CONTROL + "a"
        )
        self.driver.find_element_by_xpath('//*[@id="StartDate"]').send_keys(
            test_data_to_txt
        )

        # Select location
        self.driver.find_element_by_xpath(
            f'//option[contains(text(),"{self.test_loc}")]'
        ).click()

        # Search for appointments
        self.driver.find_element_by_xpath('//*[@id="apptSearch"]').click()

        # Search for time
        max_tries = 20
        for _ in range(max_tries):
            try:
                formatted_time = self.test_time.strftime("%-I:%M %p")
                self.driver.find_element_by_xpath(
                    f'//label[contains(text(),"{today.year} {formatted_time}")]'
                ).click()

                # Confirm appointment
                self.driver.find_element_by_xpath(
                    '//*[@id="cmdStandardProceed"]'
                ).click()
                self.driver.find_element_by_xpath('//*[@id="cmdConfirm"]').click()

                # Logging
                msg = (
                    f"Booked a test on the {test_data_to_txt} at time {formatted_time}"
                )
                print(msg)
                logger.log(msg)

                # Close driver
                self.driver.close()
                exit()
            except Exception:
                self.test_time += timedelta(minutes=5)

        # If no times were found
        err = "Sorry! There was an error booking your test, try another day."
        print(err)
        logger.error(err)

        # Quit driver
        self.driver.close()
        exit()
