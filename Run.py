import pandas as pd
from tabulate import tabulate

# Đọc dữ liệu từ file CSV
file_path = "data/filtered_data.csv"  # Đổi đường dẫn này thành file CSV của bạn
data = pd.read_csv(file_path)

# Hiển thị dữ liệu dưới dạng bảng
def display_data(df):
    print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))

# Gọi hàm để in dữ liệu
display_data(data)
