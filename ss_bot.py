# Boston University symptom survey and covid-19 appointment maker
# By Daniel Melchor (Class of 2024)
# Heavily inspired by Nic Nguyen (Class of 2024)

# Import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import time

from datetime import date
from datetime import datetime
from datetime import timedelta

# Your BU credentials
buUsername = "yourUsername"
buPassword = "yourPassword"

options = Options()

# User message
print("Completing survey...")

# Comment line under to see the procedure
options.add_argument("--headless")

# Location of your chrome driver
DRIVER_PATH = '/usr/bin/chromedriver'

# Initiate chrome and wait for load
driver = webdriver.Chrome(executable_path=DRIVER_PATH,options=options)
driver.implicitly_wait(2)

# Go to patientconnect homepage for symptom survey
driver.get('https://patientconnect.bu.edu')

# Log in (maybe accept manually the Duo verification)
loginUser = driver.find_element_by_xpath('//*[@id="j_username"]').send_keys(buUsername)
loginPass = driver.find_element_by_xpath('//*[@id="j_password"]').send_keys(buPassword)
submit = driver.find_element_by_xpath('/html/body/div[1]/div/form/button').click()

# Start survey and wait for load
completeSurveyButton = driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/form/div[3]/div/a').click()
time.sleep(0.5)

# Continue
continueButton = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[2]/div[1]/div/div[2]/a').click()

# Symptoms survey
for i in range(2,10):
    button = driver.find_element_by_xpath('//*[@id="mainbody"]/main/form/div[' + str(i) + ']/fieldset/div/div[1]/div').click()

finishSurvey = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/footer/div/div[2]/input').click()

# Symptom survey success message
print("Survey: " + driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/form/div[2]/h4').text.lower())


#------------------------------------------------------#
#------------------COVID-APPOINTMENT-------------------#
#------------------------------------------------------#

# Any date you took a test (YYYY,MM,DD)
startingDate = date(2021,3,24)

# Counting if today it should book an appointment
daysSinceLastTest = (date.today() - date(2021,3,23)).days % 4

if(daysSinceLastTest == 0):
    # User message
    print("Completing appointment...")

    driver.get('https://patientconnect.bu.edu/appointments_home.aspx')

    # Schedule button
    schedule = driver.find_element_by_xpath('//*[@id="cmdSchedule"]').click()

    # All the checkboxes pre-booking
    ids = [297,496,493,484,478,498]
    for id in ids:
        driver.find_element_by_xpath('//*[@id="' + str(id) + '"]').click()
        driver.find_element_by_xpath('//*[@id="cmdProceed"]').click()

    continueButton7 = driver.find_element_by_xpath('//*[@id="cmdStandardProceed"]').click()

    # Book 4 days ahead
    testDate = date.today() + timedelta(4)
    testDateToTxt = testDate.strftime("%m/%d/%Y")
    dateInput = driver.find_element_by_xpath('//*[@id="StartDate"]').send_keys(Keys.CONTROL + "a") # Delete by-default date
    dateInput = driver.find_element_by_xpath('//*[@id="StartDate"]').send_keys(testDateToTxt)

    # Select location
    location = 5 # Number represents the option in the dropdown menu
    selectPlace = driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/form/form/div/select/option[' + str(location) + ']').click()
    findAppointments = driver.find_element_by_xpath('//*[@id="apptSearch"]').click()

    # Book appointment from hour and minute:
    hour = 14
    minute = 0

    testDateToTxt2 = testDate.strftime("%A, %B %d, %Y")
    
    def tryBooking():
        global minute
        global hour
        global testDate
        try:
            global testDateToTxt2

            # Adjust for minutes like "4" -> "04"
            if minute < 10:
                minute = "0" + str(minute)

            # Find option with our time
            driver.find_element_by_xpath("//*[contains(text(), " + "'" + testDateToTxt2 + " " + str(hour%12) + ":" + str(minute) + " PM')]").click()
            driver.find_element_by_xpath('//*[@id="cmdStandardProceed"]').click()
            try:
                # If no error when booking -> Success
                driver.find_element_by_xpath('//*[@id="cmdConfirm"]').click()
                print("Test appointment: " + driver.find_element_by_xpath('//*[@id="mainbody"]/h1').text.lower())
            except:
                # Weird red-text error (appointment was booked already)
                confirmAppt = driver.find_element_by_xpath('//*[@id="cmdStandardCancel"]').click()

                # Try again next 5 minutes
                minute = int(minute)
                minute += 5
                if minute >= 60:
                    minute = 0
                    hour += 1
                tryBooking()
        except:
            # No option with our time -> try next 5 minutes
            minute = int(minute)
            minute += 5
            if minute >= 60:
                minute = 0
                hour += 1
            tryBooking()
            
    tryBooking()

# Wait so user can see confirmation messages
time.sleep(1)

# Close everything and exit
driver.quit()

