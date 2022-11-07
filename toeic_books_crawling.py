import imp
from msilib import type_binary
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()

options.binary_location = r"C:\Program Files\Google\Chrome Beta\Application\chrome.exe"


URL = "https://tiki.vn"

driver = webdriver.Chrome('./etc/chromedriver.exe', chrome_options=options)
# edge_driver = webdriver.Edge('./etc/msedgedriver.exe')

driver.get(URL)
sleep(10)

input = driver.find_element(By.XPATH, '//*[@id="main-header"]/div[1]/div/div[1]/div[2]/div/input') # input tìm kiếm
sleep(1)
input.send_keys("sach toeic")  # Nhập vào nội dung tìm kiếm "sach toeic"
input.send_keys(Keys.RETURN)   # Nhấn Enter
sleep(5)

# Hàm lấy URL 1 trang
def get_url():
    page_source = BeautifulSoup(driver.page_source)                     # Lấy source code trang
    product_as = page_source.find_all('a', class_='product-item')       # product_as: các thẻ a dẫn đến trang chi tiết sản phẩm
    all_product_URL = []                                                # List chứa URL
    for product_a in product_as:                                        # Lặp qua tất cả thẻ a và lấy nội dung của href
        product_URL_href = product_a.get('href')                           
        if product_URL_href.startswith('//tka.tiki.vn') == False:       # Bỏ qua các href có nội dung //tak.tiki.vn/... vì khi nối với "https://tiki.vn" tạo thành "https://tiki.vn//tak.tiki.vn/..." gây lỗi
            product_URL =  "https://tiki.vn" + product_URL_href         # product_URL_href = "/new-economy-toeic-rc-1000-p3840807.html?spid=3857621"
            if product_URL not in all_product_URL:                      # URL = "https://tiki.vn" + product_URL_href
                all_product_URL.append(product_URL)                     # --> URL = "https://tiki.vn/new-economy-toeic-rc-1000-p3840807.html?spid=3857621"
    return all_product_URL

# Hàm lấy URL nhiều trang
def get_url_all_pages(number_of_page = 3):
    URLs_all_page = []
    for page in range(number_of_page):
        URLs_one_page = get_url()
        sleep(5)
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        sleep(2)
        next_button = driver.find_element(By.CLASS_NAME, 'tikicon icon-arrow-back')
        next_button.click()
        URLs_all_page = URLs_all_page + URLs_one_page
        sleep(2)
    return URLs_all_page


product_URLs_list = get_url()
sleep(5)

# Các list chứa data thu thập được từ tất cả URL
Authors = []
Titles = []
Current_Prices = []
List_Prices = []
Discount_Rates = []
Product_URLs = []
Cty_Phat_Hanh = []
Ngay_Xuat_Ban = []
Kich_Thuoc = []
Dich_Gia = []
Loai_Bia = []
So_Trang = []
Nha_Xuat_Ban = []

for i in range(20):

# for product_URL in product_URLs_list:               # Lặp qua từng URL
    print('Crawling {}'.format(product_URLs_list[i]))
    # sleep(2)

    # Các biến chứa data thu thập được
    author = ''
    title = ''
    current_price = ''
    list_price = ''
    discount_rate = ''
    cty_phat_hanh = ''
    ngay_xuat_ban = ''
    kich_thuoc = ''
    dich_gia = ''
    loai_bia = ''
    so_trang = ''
    nha_xuat_ban = ''

    driver.get(product_URLs_list[i])
    sleep(2)                                                            
    page_source = BeautifulSoup(driver.page_source, 'html.parser')      # Lấy source code page

    content_div = page_source.find('div', class_ = 'styles__StyledProductContent-sc-1f8f774-0 ewqXRk')  # Thẻ div chứa tất cả dữ liệu cần lấy

    header_div = content_div.find('div', class_ = 'header')             # Thẻ div class='header' chứa tên tác giả, tên sách

    if header_div.find('div', class_ = 'brand'):                        # Kiểm tra thẻ div class='brand' có tồn tại
        brand = header_div.find('div', class_ = 'brand')    
        if brand.find('h6'):
            author_h6 = brand.find('h6')
            author = author_h6.find('a').get_text()                     # div class='brand' --> h6 --> a --> author
        
    title = header_div.find('h1').get_text()                            # Tên sách nằm trong thẻ h1
    
    body_div = content_div.find('div', class_ = 'body')                 # div class='body' chứa thông tin giá bán hiện tại, giá gốc và % giảm giá

    if body_div.find('div', class_ = 'product-price__current-price'):
        current_price = body_div.find('div', class_ = 'product-price__current-price').get_text()        # giá bán hiện tại nằm trong thẻ div class='product-price__current-price'

    if body_div.find('div', class_ = 'product-price__list-price'):                                  # Kiểm tra div class='product-price__list-price' có tồn tại
        list_price = body_div.find('div', class_ = 'product-price__list-price').get_text()          # Giá gốc nằm trong div class='product-price__list-price'

    if body_div.find('div', class_ = 'product-price__discount-rate'):
        discount_rate = body_div.find('div', class_ = 'product-price__discount-rate').get_text()    # % giảm nằm trong div class='product-price__discount-rate'

    # Thêm 3 giá trị vừa thu được vào list
    Current_Prices.append(current_price)
    List_Prices.append(list_price)
    Discount_Rates.append(discount_rate)
    
    '''
        Các thuộc tính Cty phát hành, ngày xuất bản, Kích thước, Dịch giả, Loại bìa, Số trang, nhà xuất bản
        nằm trong table, table --> td
        Khi lấy td của table sẽ trả về một list chứa các thẻ td
        -------------------------------------------------------
        td[0] Công ty phát hành  |  td[1] tên công ty
        td[2] Ngày xuất bản      |  td[3] ngày
        ...                      |   ...
        -------------------------------------------------------
        Do một số sản phẩm có tất cả thuộc tính, một số có ít thuộc tính hơn, một số không có thuộc tính nào
        nên lặp qua các thẻ td và gán giá trị cho các biến cty_phat_hanh, ngay_phat_hanh... có thể gặp lỗi out of range
        nên sẽ lưu các thuộc tính vào dictionary {td[0] : td[1], td[2] : td[3], ...}
        sau đó kiểm tra thuộc tính nào có trong dict mới gán giá trị cho các biến cty_phat_hanh, ngay_phat_hanh,...  
    '''
    dict_detail = {}
    if page_source.find('div', class_ = 'style__Wrapper-sc-12gwspu-0 cIWQHl'):
        detail_info_div = page_source.find('div', class_ = 'style__Wrapper-sc-12gwspu-0 cIWQHl')
        table = detail_info_div.find('table')
        td_table = table.find_all('td')
        i = 0
        while i < len(td_table):
            dict_detail[td_table[i].get_text()] = td_table[i+1].get_text()
            i+= 2

    print(dict_detail)
    
    if "Công ty phát hành" in dict_detail:
        cty_phat_hanh = dict_detail["Công ty phát hành"]
    if "Ngày xuất bản" in dict_detail:
        ngay_xuat_ban = dict_detail["Ngày xuất bản"]
    if "Kích thước" in dict_detail:
        kich_thuoc = dict_detail["Kích thước"]
    if "Dịch Giả" in dict_detail:
        dich_gia = dict_detail["Dịch Giả"]
    if "Loại bìa" in dict_detail:
        loai_bia = dict_detail["Loại bìa"]
    if "Số trang" in dict_detail:
        so_trang = dict_detail["Số trang"]
    if "Nhà xuất bản" in dict_detail:
        nha_xuat_ban = dict_detail["Nhà xuất bản"]
    
    # Thêm các giá trị vừa thu được vào list
    Authors.append(author)
    Titles.append(title)
    Cty_Phat_Hanh.append(cty_phat_hanh)
    Ngay_Xuat_Ban.append(ngay_xuat_ban)
    Kich_Thuoc.append(kich_thuoc)
    Dich_Gia.append(dich_gia)
    Loai_Bia.append(loai_bia)
    So_Trang.append(so_trang)
    Nha_Xuat_Ban.append(nha_xuat_ban)
    Product_URLs.append(product_URLs_list[i])

    print("-----> Done")


from pandas import DataFrame

data = {'Author' : Authors, 'Title' : Titles, 'Current Price' : Current_Prices, 'List Price' : List_Prices, 'Discount Rate' : Discount_Rates, 'Cong Ty Phat Hanh' : Cty_Phat_Hanh, 'Ngay Xuat Ban' : Ngay_Xuat_Ban, 'Kich Thuoc' : Kich_Thuoc, "Dich Gia" : Dich_Gia, "Loai Bia" : Loai_Bia, "So Trang" : So_Trang, "Nha Xuat Ban" : Nha_Xuat_Ban,'URL' : Product_URLs}
df = DataFrame(data, columns=['Author', 'Title', 'Current Price', 'List Price', 'Discount Rate', 'Cong Ty Phat Hanh', 'Ngay Xuat Ban', 'Kich Thuoc', 'Dich Gia', 'Loai Bia', 'So Trang', 'Nha Xuat Ban','URL'])

df.to_csv('./data/raw_toeic_books.csv', index = None, encoding='utf-8', header=True)

print("Finish Crawling")