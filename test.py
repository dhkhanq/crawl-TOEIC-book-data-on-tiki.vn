import imp
from msilib import type_binary
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup
import csv

URL = "https://tiki.vn"

driver = webdriver.Chrome('./etc/chromedriver.exe')
driver.get(URL)

search_field = driver.find_element(By.XPATH, '//*[@id="main-header"]/div[1]/div/div[1]/div[2]/div/input')
search_field.send_keys("sach toeic")
search_field.send_keys(Keys.RETURN)
sleep(15)


def get_url():
    page_source = BeautifulSoup(driver.page_source)
    product_as = page_source.find_all('a', class_='product-item') # prod_as: cac the a chua URL san pham
    all_product_URL = []
    for product_a in product_as:
        product_URL_0 = product_a.get('href')
        if product_URL_0.startswith('//tka.tiki.vn') == False:
            product_URL =  "https://tiki.vn" + product_URL_0
            if product_URL not in all_product_URL:
                all_product_URL.append(product_URL)
    return all_product_URL


author = ''
title = ''

product_URLs_list = get_url()

driver.get(product_URLs_list[0])
sleep(5)
page_source = BeautifulSoup(driver.page_source, 'html.parser')

content_div = page_source.find('div', class_ = 'styles__StyledProductContent-sc-1f8f774-0 ewqXRk')

header_div = content_div.find('div', class_ = 'header')
if header_div.find('div', class_ = 'brand'):
    brand = header_div.find('div', class_ = 'brand')
    if brand.find('h6'):
        author_h6 = brand.find('h6')
        author = author_h6.find('a').get_text()
        
title = header_div.find('h1').get_text()

print("{}, {}".format(author, title))