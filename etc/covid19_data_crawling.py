"""
ect   --> Luu driver chrome
data  --> Luu data duoc crawl 

"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
import os, time

data_save_file_csv = []

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

#driver_file_url = os.path.join('etc', 'chromedriver.exe')
driver_file_url = "./etc/chromedriver.exe"
driver = webdriver.Chrome(executable_path=driver_file_url, options=options)
driver.get("https://covid19.gov.vn/")
driver.switch_to.frame(1)

target = driver.find_elements(By.XPATH, "/html/body/div[2]/div[1]/div")
for data in target:
    cities = data.find_elements(By.CLASS_NAME, "city")
    totals = data.find_elements(By.CLASS_NAME, "total")
    days = data.find_elements(By.CLASS_NAME, "daynow")
    dies = data.find_elements(By.CLASS_NAME, "die")

cities_lst = [city.text for city in cities]
totals_lst = [total.text for total in totals]
days_lst = [day.text for day in days]
dies_lst = [die.text for die in dies]

for i in range(len(cities_lst)):
    row = "{},{},{},{}\n".format(cities_lst[i], totals_lst[i], days_lst[i], dies_lst[i])
    data_save_file_csv.append(row)

filename = "covid19"

with open(os.path.join('data',filename), 'w+', encoding='utf-8') as f:
    f.writelines(data_save_file_csv)

driver.close()

if __name__ == "__main__":
    pass