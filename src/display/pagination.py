from .table_display import display_table
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