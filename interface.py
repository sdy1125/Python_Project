import pandas as pd
from tkinter import *
from tkinter import ttk
from tkinter import simpledialog

# Đọc dữ liệu từ file CSV
file_path = "data/filtered_data.csv"
data = pd.read_csv(file_path)

# Số lượng dữ liệu trên mỗi trang
rows_per_page = 50

# Hàm hiển thị dữ liệu trong Treeview
def display_table(data, page, rows_per_page, treeview):
    total_pages = (len(data) - 1) // rows_per_page + 1
    if page < 1 or page > total_pages:
        print("Số trang không hợp lệ.")
        return
    start_index = (page - 1) * rows_per_page
    end_index = min(start_index + rows_per_page, len(data))
    page_data = data.iloc[start_index:end_index]
    
    # Thêm số thứ tự vào bảng
    page_data.insert(0, "STT", range(start_index + 1, end_index + 1))
    
    # Xóa các dòng cũ trong Treeview trước khi hiển thị dữ liệu mới
    for row in treeview.get_children():
        treeview.delete(row)
    
    # Thêm dữ liệu mới vào Treeview
    for _, row in page_data.iterrows():
        treeview.insert("", "end", values=list(row))
    
    # Cập nhật label trang
    label_page.config(text=f"Trang: {page}/{total_pages}")

# Hàm điều khiển sự kiện chuyển trang
def next_page():
    global current_page
    total_pages = (len(data) - 1) // rows_per_page + 1
    if current_page < total_pages:
        current_page += 1
        display_table(data, current_page, rows_per_page, treeview)

def prev_page():
    global current_page
    if current_page > 1:
        current_page -= 1
        display_table(data, current_page, rows_per_page, treeview)

def first_page():
    global current_page
    current_page = 1
    display_table(data, current_page, rows_per_page, treeview)

def last_page():
    global current_page
    total_pages = (len(data) - 1) // rows_per_page + 1
    current_page = total_pages
    display_table(data, current_page, rows_per_page, treeview)

def change_rows_per_page():
    global rows_per_page, current_page
    new_rows_per_page = simpledialog.askinteger("Số dòng mỗi trang", "Nhập số dòng mỗi trang:", minvalue=1)
    if new_rows_per_page:
        rows_per_page = new_rows_per_page
        current_page = 1  # Quay về trang đầu
        display_table(data, current_page, rows_per_page, treeview)

# Tạo cửa sổ Tkinter
root = Tk()
root.title("Hiển thị dữ liệu từ CSV")

# Tạo frame để chứa bảng và khung
frame_table = Frame(root)
frame_table.pack(padx=10, pady=10)

# Sử dụng Canvas để kẻ khung
canvas = Canvas(frame_table, width=800, height=400, bg='white')
canvas.pack()

# Tạo Treeview để hiển thị dữ liệu
columns = ["STT"] + list(data.columns)
treeview = ttk.Treeview(canvas, columns=columns, show="headings", height=15)

# Định nghĩa các cột trong Treeview
for col in columns:
    treeview.heading(col, text=col)
    treeview.column(col, width=100)

# Gắn Treeview vào Canvas
canvas.create_window((0, 0), window=treeview, anchor="nw")

# Cập nhật khung cho Treeview
treeview.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# Thêm label hiển thị trang
label_page = Label(root, text="Trang: 1/1")
label_page.pack(pady=5)

# Thêm nút điều khiển chuyển trang
frame_controls = Frame(root)
frame_controls.pack(pady=10)

btn_prev = Button(frame_controls, text="Trang trước", command=prev_page)
btn_prev.grid(row=0, column=0, padx=5)

btn_next = Button(frame_controls, text="Trang sau", command=next_page)
btn_next.grid(row=0, column=1, padx=5)

btn_first = Button(frame_controls, text="Đầu trang", command=first_page)
btn_first.grid(row=0, column=2, padx=5)

btn_last = Button(frame_controls, text="Cuối trang", command=last_page)
btn_last.grid(row=0, column=3, padx=5)

btn_change_rows = Button(frame_controls, text="Thay đổi số dòng mỗi trang", command=change_rows_per_page)
btn_change_rows.grid(row=0, column=4, padx=5)

# Biến toàn cục cho trang hiện tại
current_page = 1

# Hiển thị trang đầu tiên
display_table(data, current_page, rows_per_page, treeview)

# Chạy ứng dụng Tkinter
root.mainloop()
