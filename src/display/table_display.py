import pandas as pd
from tabulate import tabulate
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
