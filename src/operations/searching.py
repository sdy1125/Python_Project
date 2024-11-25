from tkinter import Tk, Toplevel, Label, Entry, Button, StringVar, ttk, messagebox
import pandas as pd

def search_data(data, root):
    """
    Tìm kiếm dữ liệu qua giao diện Tkinter.
    """
    def execute_search():
        try:
            search_type = search_type_var.get()
            keyword = keyword_var.get()

            # Xử lý tìm kiếm theo từng tiêu chí
            if search_type == "Full Name":
                result = search_by_full_name(data, keyword)
            elif search_type == "ID":
                result = search_by_id(data, keyword)
            elif search_type == "Score Threshold":
                threshold = float(keyword)
                result = search_by_all_subjects_score(data, threshold)
            elif search_type == "Extracurricular/Job":
                extracurricular = keyword.lower() == 'y'
                part_time = keyword.lower() == 'y'
                result = search_by_activities_or_job(data, extracurricular, part_time)
            else:
                messagebox.showwarning("Cảnh báo", "Chọn tiêu chí tìm kiếm hợp lệ.")
                return

            # Hiển thị kết quả tìm kiếm
            for row in tree.get_children():
                tree.delete(row)
            for _, row in result.iterrows():
                tree.insert("", "end", values=row.tolist())

        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")

    # Tạo cửa sổ tìm kiếm
    search_window = Toplevel(root)
    search_window.title("Tìm kiếm dữ liệu")
    search_window.geometry("800x600")

    # Biến lưu trữ tiêu chí và từ khóa
    search_type_var = StringVar(value="Full Name")
    keyword_var = StringVar()

    # Combobox chọn tiêu chí
    Label(search_window, text="Tiêu chí tìm kiếm:").pack(pady=5)
    search_type_menu = ttk.Combobox(search_window, textvariable=search_type_var)
    search_type_menu['values'] = ["Full Name", "ID", "Score Threshold", "Extracurricular/Job"]
    search_type_menu.pack(pady=5)

    # Input từ khóa
    Label(search_window, text="Từ khóa:").pack(pady=5)
    Entry(search_window, textvariable=keyword_var).pack(pady=5)

    # Nút tìm kiếm
    Button(search_window, text="Tìm kiếm", command=execute_search).pack(pady=10)

    # Khu vực hiển thị kết quả
    tree_frame = ttk.Frame(search_window)
    tree_frame.pack(fill="both", expand=True)

    columns = list(data.columns)
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(fill="both", expand=True)

    Button(search_window, text="Đóng", command=search_window.destroy).pack(pady=10)

# Chuyển đổi logic tìm kiếm sang hàm riêng (giữ nguyên logic)
def search_by_id(data, id_value):
    if 'id' not in data.columns:
        messagebox.showerror("Lỗi", "Cột 'id' không tồn tại trong dữ liệu.")
        return pd.DataFrame()
    return data[data['id'].astype(str).str.lower() == id_value.lower()]

def search_by_full_name(data, full_name):
    if 'first_name' not in data.columns or 'last_name' not in data.columns:
        messagebox.showerror("Lỗi", "Dữ liệu không chứa cột 'first_name' hoặc 'last_name'.")
        return pd.DataFrame()
    return data[data['first_name'].str.contains(full_name, case=False, na=False) |
                data['last_name'].str.contains(full_name, case=False, na=False)]

def search_by_all_subjects_score(data, min_score):
    subjects = ['math_score', 'history_score', 'physics_score', 
                'chemistry_score', 'biology_score', 'english_score', 'geography_score']
    missing_subjects = [subject for subject in subjects if subject not in data.columns]
    if missing_subjects:
        messagebox.showerror("Lỗi", f"Dữ liệu không chứa các cột: {', '.join(missing_subjects)}")
        return pd.DataFrame()
    return data[(data[subjects] >= min_score).all(axis=1)]

def search_by_activities_or_job(data, extracurricular=False, part_time=False):
    if 'extracurricular_activities' not in data.columns or 'part_time_job' not in data.columns:
        messagebox.showerror("Lỗi", "Dữ liệu không chứa thông tin về hoạt động ngoại khóa hoặc làm thêm.")
        return pd.DataFrame()
    if extracurricular and part_time:
        return data[(data['extracurricular_activities'] == True) | (data['part_time_job'] == True)]
    elif extracurricular:
        return data[data['extracurricular_activities'] == True]
    elif part_time:
        return data[data['part_time_job'] == True]
    else:
        return pd.DataFrame()
