from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import re
import datetime
import winsound
import logging
import pathlib

parent_directory = pathlib.Path(__file__).parent.absolute()
PATH = f'{parent_directory}\chromedriver.exe'
driver = webdriver.Chrome(PATH)

driver.get("https://public.txdpsscheduler.com/")

def convert_to_datetime(x):
    
    dateX = driver.find_element_by_xpath(x)
    date = dateX.text

    seperators = [i.start() for i in re.finditer("/", date)]
    month_day = seperators[0]
    day_yr = seperators[1]

    month = date[0:month_day]
    day = date[month_day + 1:day_yr]
    year = date[day_yr + 1: len(date)]

    #print(month)
    #print(day)

    m_int = int(month)
    d_int = int(day)
    y_int = int(year)

    return datetime.date(y_int, m_int, d_int)

def check_exist(xpath):
    try:
      exists = driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return exists

first_name = "FirstName"
last_name = "LastName"
birth_digits = "01012001"
email = "insertEmail@gmail.com"
zip_code = "99999"
ssn = "1234"

existingAppointment = False
email_input_id = 138
conf_email_id = 141
zip_code_input_id = 164


lang = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div[2]/button[1]/span')
lang.click()

F_N = driver.find_element_by_id("input-55")
F_N.send_keys(first_name)

L_N = driver.find_element_by_id("input-58")
L_N.send_keys(last_name)

DOB = driver.find_element_by_id("dob")
DOB.send_keys(birth_digits)

SSN = driver.find_element_by_id("last4Ssn")
SSN.send_keys(ssn)

driver.implicitly_wait(10) 


log_on = driver.find_element_by_xpath('//*[@id="app"]/section/div/main/div/section/div[2]/div/div/form/div[2]/div[4]/button/span') 
log_on.click()

driver.implicitly_wait(10) 
new_appointment = driver.find_element_by_xpath('//*[@id="app"]/section/div/main/div/section/div[2]/div/div/div[3]/div/button')
new_appointment.click()

if check_exist('//*[@id="app"]/div[1]/div/div/div[2]/button/span'):
    existingAppointment = True

if existingAppointment:
    appointment_exists = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/div/div[2]/button/span')
    appointment_exists.click()
elif not existingAppointment: 
    email_input_id -= 4
    conf_email_id -= 4
    zip_code_input_id -= 4 
    pass
else:
    print("error, cannot detrmine xpath eligibility")


apply_permit = driver.find_element_by_xpath('//*[@id="app"]/section/div/main/div/section/div[2]/div/main/div/div/div[1]/div[1]/button')
apply_permit.click()

email_input = driver.find_element_by_id(f"input-{email_input_id}")
email_input.send_keys(email)

conf_email = driver.find_element_by_id(f"input-{conf_email_id}")
conf_email.send_keys(email)

zip_code_input = driver.find_element_by_id(f"input-{zip_code_input_id}")
zip_code_input.send_keys(zip_code)


while True:

    next = driver.find_element_by_xpath('//*[@id="app"]/section/div/main/div/section/div[2]/div/form/div/div[2]/div[2]/div/div[2]/button/span')
    next.click()

    new_Second = convert_to_datetime('//*[@id="app"]/section/div/main/div/section/div[2]/div/div[2]/div/table/tbody/tr[1]/td[3]')

    new_Closest = convert_to_datetime('//*[@id="app"]/section/div/main/div/section/div[2]/div/div[1]/div/table/tbody/tr/td[3]')

    #format: (year, month, day)
    current = datetime.date(2022, 7, 26)

    print(f'Closest: {new_Closest} SecondClosest: {new_Second}')

    if (new_Second < current and new_Second > datetime.date(2022, 7, 20)):
        print(new_Second)
        duration = 2500  # milliseconds
        freq = 440  # Hz
        winsound.Beep(freq, duration)
        break    
    else:
        time.sleep(3)
        previous = driver.find_element_by_xpath('//*[@id="app"]/section/div/main/div/section/div[2]/div/div[5]/div/div[1]/button/span/i')
        previous.click()