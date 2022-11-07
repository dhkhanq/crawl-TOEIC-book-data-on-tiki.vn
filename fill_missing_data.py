import pandas as pd

data = pd.read_csv("./data/raw_toeic_books.csv")

# Drop row if its have null value > 5
new_data = data.dropna(axis=0, thresh=data.shape[1]-5)

# replace null value of author to 'Tác giả: Not Provided'
new_data["Author"].fillna("Not Provided", inplace=True)
# replace null value of List Price to value from current Price
new_data["List Price"].fillna(new_data["Current Price"], inplace=True)
# replace null value of Discount Rate to '0%'
new_data["Discount Rate"].fillna("-0%", inplace=True)
# replace null value of Ngay Xuat Ban to 'Not Provided'
new_data["Ngay Xuat Ban"].fillna("Not Provided", inplace=True)
# replace null value of Loai Bia to 'Not Provided'
new_data["Loai Bia"].fillna("Not Provided", inplace=True)
# replace null value of Kich Thuoc to 'Not Provided'
new_data["Kich Thuoc"].fillna("Not Provided", inplace=True)
# replace null value of So Trang to 'Not Provided'
new_data["So Trang"].fillna("Not Provided", inplace=True)
# replace null value of Nha Xuat Ban to 'Not Provided'
new_data["Nha Xuat Ban"].fillna("Not Provided", inplace=True)
# replace null value of Dich Gia to 'Not Provided'
new_data["Dich Gia"].fillna("Not Provided", inplace=True)


# Replace current csv file
new_data.to_csv('./data/toeic_books.csv', index=None, header=True, encoding='utf-8')