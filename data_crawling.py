from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from pandas import DataFrame, NA
from time import sleep

def crawl(URL):
    driver = webdriver.Chrome('driver\chromedriver-win64\chromedriver.exe') # Chrome Driver for version 120.0.6099
    driver.get(URL)
    sleep(2)

    input = driver.find_element(By.CLASS_NAME, 'styles__InputRevamp-sc-6cbqeh-2')
    input.send_keys("sach toeic")
    input.send_keys(Keys.RETURN)
    sleep(2)

    data = { 'Tên': [], 'Giá': [], 'Giảm giá': [], 'Đã bán': [], 'Tác giả': [], "Công ty phát hành": [], "Loại bìa": [], "Nhà bán": [], "Link": [] }

    while True:
        a_tags = driver.find_elements(By.CLASS_NAME, 'product-item')
        for a in a_tags:
            product = {}

            url = a.get_property('href')
            product['Link'] = url

            # Get book name
            if len(a.find_elements(By.CLASS_NAME, 'product-name')) != 0:
                product['Tên'] = a.find_element(By.CLASS_NAME, 'product-name').text
            else:
                product['Tên'] = NA
            
            # Get book price
            product['Giá'] = a.find_element(By.CLASS_NAME, 'price-discount__price').text

            # Get discount percentage of product
            if len(a.find_elements(By.CLASS_NAME, 'price-discount__percent')) != 0:
                product['Giảm giá'] = a.find_element(By.CLASS_NAME, 'price-discount__percent').text
            else:
                product['Giảm giá'] = NA

            # Get number of books sold
            if len(a.find_elements(By.CLASS_NAME, 'quantity')) != 0:
                product['Đã bán'] = a.find_element(By.CLASS_NAME, 'quantity').text
            else:
                product['Đã bán'] = NA
            
            # Get author of book
            if len(a.find_elements(By.CLASS_NAME, 'hjPFIz')) != 0:
                product['Tác giả'] = a.find_element(By.CLASS_NAME, 'hjPFIz').text
            else:
                product['Tác giả'] = NA

            # Get more infomation of book
            info_divs = a.find_element(By.CLASS_NAME, 'under-rating-v2').find_elements(By.CLASS_NAME, 'iFrjUu')
            for div in info_divs:
                spans = div.find_elements(By.TAG_NAME, 'span')
                key = spans[0].text.rstrip(':')
                value = spans[1].text
                product[key] = value
            
            for key in data:
                if key in product:
                    data[key].append(product[key])
                else:
                    data[key].append(NA)

        try:
            arrow = driver.find_element(By.CLASS_NAME, 'undefined')
            arrow.click()
            sleep(2)
        except NoSuchElementException:
            break
    
    print("Crawling data successfully!")
    return data

if __name__ == "__main__":
    data = crawl("https://tiki.vn")
    print("Saving file...")
    df = DataFrame(data)
    df.to_csv("./data/data.csv", index = None, encoding='utf-8', header=True)
    print("Successed!")
