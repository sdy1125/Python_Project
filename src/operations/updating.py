from tkinter import Toplevel, Label, Entry, Button, StringVar, messagebox, Frame
import pandas as pd
rows_per_page=50
def update_data_by_id(data, file_path, root):
    from src.display.table_display import create_table_window
    """
    Cập nhật toàn bộ dữ liệu thuộc hàng có ID được chọn qua giao diện Tkinter.
    :param data: DataFrame chứa dữ liệu
    :param file_path: Đường dẫn file CSV để lưu thay đổi
    :param root: Cửa sổ chính Tkinter
    :param current_page: Trang hiện tại
    :param rows_per_page: Số dòng mỗi trang
    :param treeview: Widget Treeview hiển thị bảng dữ liệu
    :param label_page: Nhãn hiển thị số trang
    """
    id_column = "id"  # Mặc định cột ID là "id"

    if id_column not in data.columns:
        messagebox.showerror("Lỗi", f"Cột '{id_column}' không tồn tại trong dữ liệu.")
        return

    column_headers_vietnamese = {
        "full_name": "Họ và Tên",
        "gender": "Giới tính",
        "part_time_job": "Công việc làm thêm",
        "weekly_self_study_hours": "Giờ tự học mỗi tuần",
        "math_score": "Điểm Toán",
        "history_score": "Điểm Lịch sử",
        "physics_score": "Điểm Vật lý",
        "chemistry_score": "Điểm Hóa học",
        "biology_score": "Điểm Sinh học",
        "english_score": "Điểm Tiếng Anh",
        "geography_score": "Điểm Địa lý"
    }

    # Tạo cửa sổ cập nhật
    update_window = Toplevel(root)
    update_window.title("Cập nhật dữ liệu")
    update_window.geometry("300x900")

    # Biến lưu trữ ID và giá trị mới
    search_id_var = StringVar()
    update_vars = {col: StringVar() for col in data.columns if col != id_column and col != "average_score"}

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
                        # Kiểm tra giá trị điểm: Đảm bảo giá trị là số thực và không vượt quá 100
                        if col.endswith('_score') or col == 'average_score':
                            if not new_value.replace('.', '', 1).isdigit():
                                messagebox.showwarning("Cảnh báo", f"Giá trị cho cột '{column_headers_vietnamese.get(col, col)}' phải là một số hợp lệ.")
                                return
                            new_value = float(new_value) if '.' in new_value else int(new_value)
                            if not (0 <= new_value <= 100):
                                messagebox.showwarning(
                                    "Cảnh báo",
                                    f"Điểm của cột '{column_headers_vietnamese.get(col, col)}' phải nằm trong khoảng từ 0 đến 100."
                                )
                                return  # Dừng lại nếu điểm không hợp lệ
                        if col == "weekly_self_study_hours":
                            new_value = float(new_value) if '.' in new_value else int(new_value)
                            if not (0 <= new_value <= 168):
                                messagebox.showwarning(
                                    "Cảnh báo",
                                    f"Số giờ tự học phải nằm trong khoảng từ 0 đến 168."
                                )
                                return
                        if col == "gender":
                            if new_value.lower() not in ["male", "female"]:
                                messagebox.showwarning(
                                    "Cảnh báo",
                                    f"Giá trị của cột '{column_headers_vietnamese.get(col, col)}' phải là 'male' hoặc 'female'."
                                 )
                                return
                
                        # Kiểm tra giá trị "Công việc làm thêm" (True/False)
                        if col == "part_time_job":
                            if new_value.lower() not in ["true", "false"]:
                                messagebox.showwarning("Cảnh báo", f"Giá trị của cột '{column_headers_vietnamese.get(col, col)}' phải là 'true' hoặc 'false'.")
                                return  # Dừng lại nếu giá trị không hợp lệ
                            new_value = new_value.lower() == "true"

                        # Cập nhật dữ liệu
                        data.at[row_index, col] = new_value
                    except ValueError as e:
                        messagebox.showwarning(
                            "Cảnh báo",
                            f"Giá trị không hợp lệ cho cột '{column_headers_vietnamese.get(col, col)}'. Lý do: {str(e)}"
                        )
                        return  # Dừng lại và yêu cầu người dùng sửa lỗi

            # Tính lại Điểm Trung bình từ các cột điểm
            score_columns = ['math_score', 'history_score', 'physics_score', 'chemistry_score', 
                             'biology_score', 'english_score', 'geography_score']
            scores = [data.at[row_index, col] for col in score_columns if pd.notna(data.at[row_index, col])]
            if scores:
                average_score = round(sum(scores) / len(scores), 2)  # Làm tròn đến 2 chữ số thập phân
                if average_score < 0 or average_score > 100:
                    messagebox.showwarning("Cảnh báo", "Điểm trung bình phải nằm trong khoảng từ 0 đến 100.")
                    return  # Ngừng cập nhật nếu điểm trung bình không hợp lệ
                data.at[row_index, 'average_score'] = average_score

            # Lưu vào file CSV
            data.to_csv(file_path, index=False)
            messagebox.showinfo("Thành công", f"Dữ liệu đã được lưu vào '{file_path}'.")
            update_window.destroy()

            # Refresh table after saving changes
            create_table_window(data, rows_per_page)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi lưu dữ liệu: {e}")


    # Form nhập ID
    Label(update_window, text="Nhập ID để cập nhật:").pack(pady=5)
    Entry(update_window, textvariable=search_id_var).pack(pady=5)

    # Tạo một Frame để chứa các nút "Tải dữ liệu" và "Lưu thay đổi" nằm ngang
    button_frame = Frame(update_window)
    button_frame.pack(pady=10)

    Button(button_frame, text="Tải dữ liệu", command=load_row).pack(side="left", padx=5)
    Button(button_frame, text="Lưu thay đổi", command=save_changes).pack(side="left", padx=5)

    # Form cập nhật dữ liệu
    Label(update_window, text="Cập nhật thông tin:").pack(pady=10)
    for col, var in update_vars.items():
        label_text = column_headers_vietnamese.get(col, col)
        Label(update_window, text=f"{label_text}:").pack(pady=2)
        Entry(update_window, textvariable=var).pack(pady=2)
