import csv

# Đường dẫn đến file CSV
file_path = 'data/data.csv'

# Đọc dữ liệu từ file CSV và in ra
with open(file_path, mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    # Đọc dòng tiêu đề (header)
    header = next(csv_reader)
    print(header)

    # Đọc và in các dòng dữ liệu
    for row in csv_reader:
        print(row)
