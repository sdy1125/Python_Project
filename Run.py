import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Đường dẫn đến file CSV có sẵn
file_path = "data/filtered_data.csv"  # Đổi thành đường dẫn đến file của bạn

# Hàm để tải và hiển thị dữ liệu từ file CSV
def load_csv():
    try:
        df = pd.read_csv(file_path)
        display_data(df)
    except Exception as e:
        messagebox.showerror("Error", f"Could not load file:\n{e}")

# Hàm để hiển thị dữ liệu trong bảng
def display_data(df):
    # Xóa dữ liệu cũ
    for row in tree.get_children():
        tree.delete(row)

    # Đặt tiêu đề cột
    tree["columns"] = list(df.columns)
    tree["show"] = "headings"

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    # Thêm dữ liệu vào bảng
    for index, row in df.iterrows():
        tree.insert("", "end", values=list(row))

# Tạo giao diện chính
root = tk.Tk()
root.title("Dữ liệu sinh viên")
root.geometry("800x600")

# Tạo bảng để hiển thị dữ liệu
frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

tree = ttk.Treeview(frame)
tree.pack(fill="both", expand=True, side="left")

# Thanh cuộn
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
scrollbar.pack(side="right", fill="y")
tree.configure(yscroll=scrollbar.set)

# Tự động tải file khi chạy chương trình
load_csv()

# Khởi động giao diện
root.mainloop()
