from tkinter import Toplevel, Label, Button, ttk, StringVar, messagebox
import pandas as pd
from src.display.table_display import create_table_window  # Hàm hiển thị dữ liệu với Treeview và phân trang

def sort_data(data, rows_per_page, root):
    """
    Sắp xếp dữ liệu qua giao diện Tkinter.
    """
    def execute_sort():
        try:
            # Lấy lựa chọn từ người dùng
            column_choice = column_var.get()
            if column_choice == "Giờ tự học/tuần":
                column_name = "weekly_self_study_hours"
            elif column_choice == "Điểm trung bình":
                column_name = "average_score"
            else:
                messagebox.showwarning("Cảnh báo", "Chọn tiêu chí sắp xếp hợp lệ.")
                return

            # Xác định thứ tự sắp xếp (tăng/giảm)
            ascending = sort_order_var.get() == "Tăng dần"

            # Sắp xếp dữ liệu
            sorted_data = data.sort_values(by=column_name, ascending=ascending)
            messagebox.showinfo("Thành công", f"Dữ liệu đã được sắp xếp theo '{column_choice}'.")

            # Gọi hàm hiển thị dữ liệu đã sắp xếp
            create_table_window(sorted_data, rows_per_page)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")

    # Tạo cửa sổ sắp xếp
    sort_window = Toplevel(root)
    sort_window.title("Sắp xếp dữ liệu")
    sort_window.geometry("400x300")

    # Biến lưu trữ lựa chọn cột và thứ tự sắp xếp
    column_var = StringVar(value="Giờ tự học/tuần")
    sort_order_var = StringVar(value="Tăng dần")

    # Nhãn và combobox chọn tiêu chí sắp xếp
    Label(sort_window, text="Chọn tiêu chí sắp xếp:").pack(pady=5)
    column_menu = ttk.Combobox(sort_window, textvariable=column_var)
    column_menu['values'] = ["Giờ tự học/tuần", "Điểm trung bình"]
    column_menu.pack(pady=5)

    # Nhãn và combobox chọn thứ tự sắp xếp
    Label(sort_window, text="Chọn thứ tự sắp xếp:").pack(pady=5)
    order_menu = ttk.Combobox(sort_window, textvariable=sort_order_var)
    order_menu['values'] = ["Giảm dần", "Tăng dần"]
    order_menu.pack(pady=5)

    # Nút thực hiện sắp xếp
    Button(sort_window, text="Sắp xếp", command=execute_sort).pack(pady=20)

    # Nút đóng cửa sổ
    Button(sort_window, text="Đóng", command=sort_window.destroy).pack(pady=10)
