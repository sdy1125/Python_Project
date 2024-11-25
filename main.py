import pandas as pd
import tkinter as tk
from tkinter import ttk
from src.display.table_display import create_table_window
from src.operations.sorting import sort_data
from src.operations.updating import update_data_by_id
from src.operations.add_and_delete import menu_update
from src.operations.searching import search_data

# Đường dẫn file CSV
file_path = "data/filtered_data.csv"
data = pd.read_csv(file_path)

# Số dòng hiển thị trên mỗi trang
rows_per_page = 50
current_page =1


def display_data_tk():
   create_table_window(data, rows_per_page=50)

def menu_sort_data():
    """
    Gọi chức năng sắp xếp dữ liệu.
    """
    sort_data(data, rows_per_page,root)

def menu_update_data():
    """
    Gọi chức năng cập nhật dữ liệu.
    """
    update_data_by_id(data, file_path, root)

def menu_add_delete():
    """
    Gọi chức năng thêm và xóa dữ liệu.
    """
    menu_update(file_path)

def menu_search_data():
    """
    Gọi chức năng tìm kiếm dữ liệu.
    """
    search_data(data, root)

# Giao diện chính
root = tk.Tk()
root.title("Hệ thống quản lý dữ liệu")
root.geometry("600x400")

tk.Button(root, text="Hiển thị danh sách dữ liệu", command=display_data_tk).pack(pady=10)
tk.Button(root, text="Sắp xếp dữ liệu", command=menu_sort_data).pack(pady=10)
tk.Button(root, text="Cập nhật dữ liệu", command=menu_update_data).pack(pady=10)
tk.Button(root, text="Thêm/Xóa dữ liệu", command=menu_add_delete).pack(pady=10)
tk.Button(root, text="Tìm kiếm dữ liệu", command=menu_search_data).pack(pady=10)

root.mainloop()
