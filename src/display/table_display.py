import pandas as pd
from tkinter import Toplevel, Label, Button, Frame, ttk, simpledialog


def display_table(data, current_page, rows_per_page, treeview, label_page):
    """
    Hiển thị dữ liệu trong Treeview với phân trang.
    """
    total_pages = (len(data) - 1) // rows_per_page + 1
    if current_page < 1 or current_page > total_pages:
        return

    start_index = (current_page - 1) * rows_per_page
    end_index = min(start_index + rows_per_page, len(data))
    page_data = data.iloc[start_index:end_index]

    # Thêm số thứ tự (STT)
    page_data.insert(0, "STT", range(start_index + 1, end_index + 1))

    # Xóa dữ liệu cũ trong Treeview
    for row in treeview.get_children():
        treeview.delete(row)

    # Thêm dữ liệu mới
    for _, row in page_data.iterrows():
        treeview.insert("", "end", values=row.tolist())

    # Cập nhật thông tin trang
    label_page.config(text=f"Trang: {current_page}/{total_pages}")


def create_table_window(data, rows_per_page=50):
    """
    Tạo cửa sổ hiển thị dữ liệu với Treeview và phân trang.
    """
    root = Toplevel()
    root.title("Hiển thị dữ liệu")
    root.geometry("1960x600")

    # Frame chứa bảng
    frame_table = Frame(root)
    frame_table.pack(padx=10, pady=10)

    # Treeview hiển thị dữ liệu
    columns = ["STT"] + list(data.columns)
    treeview = ttk.Treeview(frame_table, columns=columns, show="headings", height=20)

# Tạo từ điển ánh xạ tiêu đề cột sang tiếng Việt
    column_headers_vietnamese = {
     "STT": "STT",
     "id": "Mã số",
     "full_name": "Họ và Tên",
     "gender": "Giới tính",
     "part_time_job": "Công việc làm thêm",
     "weekly_self_study_hours": "Giờ tự học/tuần",
     "math_score": "Điểm Toán",
     "history_score": "Điểm Lịch sử",
     "physics_score": "Điểm Vật lý",
     "chemistry_score": "Điểm Hóa học",
     "biology_score": "Điểm Sinh học",
     "english_score": "Điểm Tiếng Anh",
     "geography_score": "Điểm Địa lý",
     "average_score": "Điểm Trung bình"
    }
# Gán tiêu đề tiếng Việt vào cột
    for col in columns:
      treeview.heading(col, text=column_headers_vietnamese.get(col, col))  # Lấy tiêu đề tiếng Việt nếu có, nếu không giữ nguyên
      treeview.column(col, width=100, anchor="center")
    treeview.pack(fill="both", expand=True)

    # Biến toàn cục cho trạng thái trang hiện tại
    current_page = [1]  # Sử dụng danh sách để giữ tham chiếu mutable

    # Label hiển thị trạng thái trang
    label_page = Label(root, text=f"Trang: {current_page[0]}/1")
    label_page.pack(pady=5)

    # Phương thức chuyển trang
    def next_page():
        total_pages = (len(data) - 1) // rows_per_page + 1
        if current_page[0] < total_pages:
            current_page[0] += 1
            display_table(data, current_page[0], rows_per_page, treeview, label_page)

    def prev_page():
        if current_page[0] > 1:
            current_page[0] -= 1
            display_table(data, current_page[0], rows_per_page, treeview, label_page)

    def first_page():
        current_page[0] = 1
        display_table(data, current_page[0], rows_per_page, treeview, label_page)

    def last_page():
        total_pages = (len(data) - 1) // rows_per_page + 1
        current_page[0] = total_pages
        display_table(data, current_page[0], rows_per_page, treeview, label_page)

    def change_rows_per_page():
        nonlocal rows_per_page
        new_rows = simpledialog.askinteger("Số dòng mỗi trang", "Nhập số dòng mỗi trang:", minvalue=1)
        if new_rows:
            rows_per_page = new_rows
            current_page[0] = 1  # Reset về trang đầu
            display_table(data, current_page[0], rows_per_page, treeview, label_page)

    # Frame chứa nút điều hướng
    frame_controls = Frame(root)
    frame_controls.pack(pady=10)

    Button(frame_controls, text="Trang trước", command=prev_page).grid(row=0, column=0, padx=5)
    Button(frame_controls, text="Trang sau", command=next_page).grid(row=0, column=1, padx=5)
    Button(frame_controls, text="Đầu trang", command=first_page).grid(row=0, column=2, padx=5)
    Button(frame_controls, text="Cuối trang", command=last_page).grid(row=0, column=3, padx=5)
    Button(frame_controls, text="Thay đổi số dòng mỗi trang", command=change_rows_per_page).grid(row=0, column=4, padx=5)
    Button(frame_controls, text="Đóng cửa sổ", command=root.destroy).grid(row=0, column=5, padx=5)
    # Hiển thị trang đầu tiên
    display_table(data, current_page[0], rows_per_page, treeview, label_page)
