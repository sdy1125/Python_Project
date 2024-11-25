from tkinter import Toplevel, Label, Entry, Button, StringVar, messagebox
import pandas as pd

def update_data_by_id(data, file_path, root):
    """
    Cập nhật toàn bộ dữ liệu thuộc hàng có ID được chọn qua giao diện Tkinter.
    :param data: DataFrame chứa dữ liệu
    :param file_path: Đường dẫn file CSV để lưu thay đổi
    :param root: Cửa sổ chính Tkinter
    """
    id_column = "id"  # Mặc định cột ID là "ID"

    if id_column not in data.columns:
        messagebox.showerror("Lỗi", f"Cột '{id_column}' không tồn tại trong dữ liệu.")
        return

    # Tạo cửa sổ cập nhật
    update_window = Toplevel(root)
    update_window.title("Cập nhật dữ liệu")
    update_window.geometry("500x400")

    # Biến lưu trữ ID và giá trị mới
    search_id_var = StringVar()
    update_vars = {col: StringVar() for col in data.columns if col != id_column}

    def load_row():
        search_id = search_id_var.get()
        try:
            # Kiểm tra kiểu ID
            search_id_value = int(search_id) if data[id_column].dtype in ['int64', 'float64'] else search_id
            matching_rows = data[data[id_column] == search_id_value]

            if matching_rows.empty:
                messagebox.showerror("Lỗi", f"Không tìm thấy dữ liệu với ID = {search_id}.")
                return

            row_index = matching_rows.index[0]
            row_data = matching_rows.iloc[0]

            # Hiển thị giá trị hiện tại
            for col, var in update_vars.items():
                var.set(row_data[col])

        except ValueError:
            messagebox.showerror("Lỗi", "ID không hợp lệ. Vui lòng nhập đúng định dạng.")

    def save_changes():
        search_id = search_id_var.get()
        try:
            # Kiểm tra kiểu ID
            search_id_value = int(search_id) if data[id_column].dtype in ['int64', 'float64'] else search_id
            row_index = data[data[id_column] == search_id_value].index[0]

            # Cập nhật giá trị mới
            for col, var in update_vars.items():
                new_value = var.get()
                if new_value:
                    try:
                        # Chuyển kiểu dữ liệu nếu cần
                        if pd.api.types.is_numeric_dtype(data[col]):
                            new_value = float(new_value) if '.' in new_value else int(new_value)
                        data.at[row_index, col] = new_value
                    except ValueError:
                        messagebox.showwarning("Cảnh báo", f"Giá trị không hợp lệ cho cột '{col}'. Giữ nguyên giá trị cũ.")

            # Lưu vào file CSV
            data.to_csv(file_path, index=False)
            messagebox.showinfo("Thành công", f"Dữ liệu đã được lưu vào '{file_path}'.")
            update_window.destroy()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")

    # Form nhập ID
    Label(update_window, text="Nhập ID để cập nhật:").pack(pady=5)
    Entry(update_window, textvariable=search_id_var).pack(pady=5)
    Button(update_window, text="Tải dữ liệu", command=load_row).pack(pady=10)

    # Form cập nhật dữ liệu
    Label(update_window, text="Cập nhật thông tin:").pack(pady=10)
    for col, var in update_vars.items():
        Label(update_window, text=f"{col}:").pack(pady=2)
        Entry(update_window, textvariable=var).pack(pady=2)

    # Nút lưu thay đổi
    Button(update_window, text="Lưu thay đổi", command=save_changes).pack(pady=20)

