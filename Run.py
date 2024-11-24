import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt

# Đọc dữ liệu từ file CSV
file_path = "data/filtered_data.csv"
data = pd.read_csv(file_path)

# Số lượng dữ liệu trên mỗi trang
rows_per_page = 50

# Chức năng 1: Hiển thị dữ liệu theo dạng bảng với phân trang
def display_table(data, page, rows_per_page):
    total_pages = (len(data) - 1) // rows_per_page + 1
    if page < 1 or page > total_pages:
        print("Số trang không hợp lệ.")
        return
    start_index = (page - 1) * rows_per_page
    end_index = min(start_index + rows_per_page, len(data))
    page_data = data.iloc[start_index:end_index].copy()
    page_data.insert(0, "STT", range(start_index + 1, end_index + 1))
    print("=" * 80)
    print(f"Hiển thị từ dòng {start_index + 1} đến {end_index} trên tổng {len(data)} dữ liệu".center(80))
    print(f"Trang: {page}/{total_pages}".center(80))
    print("=" * 80)
    print(tabulate(page_data, headers="keys", tablefmt="grid", showindex=False))
    print("=" * 80)

# Chức năng phân trang cho chức năng hiển thị
def paginate_data(data, rows_per_page):
    current_page = 1
    total_pages = (len(data) - 1) // rows_per_page + 1
    while True:
        display_table(data, current_page, rows_per_page)
        print("\n* Các lệnh điều khiển *")
        print("n: trang tiếp    p: trang trước")
        print("f: đến trang đầu l: đến trang cuối")
        print("s: đổi số lượng hiển thị mỗi trang")
        print("q: thoát")
        print("-" * 80)
        command = input("Nhập lệnh: ").strip().lower()
        if command == 'n':
            if current_page < total_pages:
                current_page += 1
            else:
                print("Đây là trang cuối.")
        elif command == 'p':
            if current_page > 1:
                current_page -= 1
            else:
                print("Đây là trang đầu.")
        elif command == 'f':
            current_page = 1
        elif command == 'l':
            current_page = total_pages
        elif command == 's':
            try:
                new_rows_per_page = int(input("Nhập số dòng trên mỗi trang: "))
                if new_rows_per_page > 0:
                    rows_per_page = new_rows_per_page
                    total_pages = (len(data) - 1) // rows_per_page + 1
                    current_page = 1  # Quay về trang đầu
                else:
                    print("Số dòng phải lớn hơn 0.")
            except ValueError:
                print("Vui lòng nhập một số hợp lệ.")
        elif command == 'q':
            print("Thoát chức năng hiển thị.")
            break
        else:
            print("Lệnh không hợp lệ. Vui lòng thử lại.")

# Chức năng 2: Sắp xếp dữ liệu
def sort_data(data):
    column = input("Nhập tên cột muốn sắp xếp: ").strip()
    order = input("Sắp xếp tăng (asc) hay giảm (desc): ").strip().lower()
    if column in data.columns:
        ascending = True if order == 'asc' else False
        sorted_data = data.sort_values(by=column, ascending=ascending)
        print("Dữ liệu sau khi sắp xếp:")
        paginate_data(sorted_data, rows_per_page)
    else:
        print("Cột không hợp lệ.")

# Chức năng 3: Tìm kiếm dữ liệu
# def search_data(data):

# Chức năng 4: Thêm dữ liệu
# def add_data(data):

# Chức năng 5: Cập nhật dữ liệu
# def update_data(data):


# Chức năng 6: Xóa dữ liệu
# def delete_data(data):


# Chức năng 7: Hiển thị biểu đồ
# def plot_data(data):

def main():
    global data
    while True:
        print("========MENU========")
        print("1. Hiển thị danh sách dữ liệu")
        print("2. Sắp xếp dữ liệu")
        print("3. Tìm kiếm dữ liệu")
        print("4. Thêm dữ liệu")
        print("5. Cập nhật dữ liệu được chọn")
        print("6. Xóa dữ liệu")
        print("7. Hiển thị biểu đồ")
        print("0. Thoát chương trình")
        print("====================")
        
        choice = input("Nhập lựa chọn: ").strip()
        
        if choice == '1':
            paginate_data(data, rows_per_page)
        elif choice == '2':
            sort_data(data)
        elif choice == '3':
            search_data(data)
        elif choice == '4':
            data = add_data(data)
        elif choice == '5':
            data = update_data(data)
        elif choice == '6':
            data = delete_data(data)
        elif choice == '7':
            plot_data(data)
        elif choice == '0':
            print("Thoát chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")

if __name__ == "__main__":
    main()
