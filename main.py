from src.display.pagination import paginate_data
from src.operations.sorting import sort_data
from src.operations.updating import update_data_by_id
from src.operations.add_and_delete import menu_add_and_delete
from src.operations.searching import search_data
import pandas as pd

file_path = "data/filtered_data.csv"
data = pd.read_csv(file_path)
rows_per_page = 50

def main():
    global data
    while True:
        print("========MENU========")
        print("1. Hiển thị danh sách dữ liệu")
        print("2. Sắp xếp dữ liệu")
        print("3. Tìm kiếm dữ liệu")
        print("4. Cập nhật dữ liệu được chọn")
        print("5. Thêm dữ liệu và xóa dữ liệu")
        print("6. Hiển thị biểu đồ")
        print("0. Thoát chương trình")
        print("====================")
        
        choice = input("Nhập lựa chọn: ").strip()
        
        if choice == '1':
            paginate_data(data, rows_per_page)
        elif choice == '2':
            data = sort_data(data, rows_per_page)
        elif choice == '3':
            search_data(data)
        elif choice == '4':
          data = update_data_by_id(data, file_path)
        elif choice == '5':
            data = menu_add_and_delete(file_path)
            data = pd.read_csv(file_path)
        elif choice == '6':
            plot_data(data)
        elif choice == '0':
            print("Thoát chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")

if __name__ == "__main__":
    main()
