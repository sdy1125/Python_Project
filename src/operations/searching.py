from tkinter import Tk, Toplevel, Label, Entry, Button, StringVar, ttk, messagebox
import pandas as pd
def search_data(data, root):
    """
    Tìm kiếm dữ liệu qua giao diện Tkinter (hiển thị tiếng Việt).
    """
    def execute_search():
        file_path = "data/filtered_data.csv"
        data = pd.read_csv(file_path)
        try:
            search_type = search_type_var.get()
            keyword = keyword_var.get()

            # Xử lý tìm kiếm theo từng tiêu chí
            if search_type == "Họ và Tên":
                result = search_by_full_name(data, keyword)
            elif search_type == "ID":
                result = search_by_id(data, keyword)
            elif search_type == "Ngưỡng Điểm":
                threshold = float(keyword)
                result = search_by_all_subjects_score(data, threshold)
            elif search_type == "Công việc/Hoạt động":
                if keyword.lower() in ['có', 'không', 'true', 'false']:
                    part_time = keyword.lower() in ['có', 'true']
                    result = search_by_activities_or_job(data, part_time)
                else:
                    messagebox.showwarning("Cảnh báo", "Vui lòng nhập 'Có' hoặc 'Không' cho tiêu chí này.")
                    return

            # Hiển thị kết quả tìm kiếm
            for row in tree.get_children():
                tree.delete(row)
            for _, row in result.iterrows():
                tree.insert("", "end", values=row.tolist())

        except ValueError:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đúng định dạng cho từ khóa tìm kiếm.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")

    # Tạo cửa sổ tìm kiếm
    search_window = Toplevel(root)
    search_window.title("Tìm kiếm dữ liệu")
    search_window.geometry("1600x600")
    

    # Biến lưu trữ tiêu chí và từ khóa
    search_type_var = StringVar(value="Họ và Tên")
    keyword_var = StringVar()

    # Combobox chọn tiêu chí
    Label(search_window, text="Tiêu chí tìm kiếm:").pack(pady=5)
    search_type_menu = ttk.Combobox(search_window, textvariable=search_type_var)
    search_type_menu['values'] = ["Họ và Tên", "ID", "Ngưỡng Điểm", "Công việc/Hoạt động"]
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
    # Ánh xạ tên cột sang tiếng Việt
    column_headers_vietnamese = {
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
        "average_score": "Điểm Trung bình",
    }

    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=column_headers_vietnamese.get(col, col))  # Hiển thị tiếng Việt nếu có
        tree.column(col, width=100)
    tree.pack(fill="both", expand=True)

    # Nút đóng
    Button(search_window, text="Đóng", command=search_window.destroy).pack(pady=10)

# Các hàm tìm kiếm (giữ nguyên logic)
def search_by_id(data, id_value):
    if 'id' not in data.columns:
        messagebox.showerror("Lỗi", "Cột 'Mã số' không tồn tại trong dữ liệu.")
        return pd.DataFrame()
    return data[data['id'].astype(str).str.lower() == id_value.lower()]

def search_by_full_name(data, full_name_input):
    return data[data['full_name'].str.contains(full_name_input, case=False, na=False)]

def search_by_all_subjects_score(data, min_score):
    subjects = ['math_score', 'history_score', 'physics_score', 
                'chemistry_score', 'biology_score', 'english_score', 'geography_score']
    missing_subjects = [subject for subject in subjects if subject not in data.columns]
    if missing_subjects:
        messagebox.showerror("Lỗi", f"Dữ liệu không chứa các cột: {', '.join(missing_subjects)}")
        return pd.DataFrame()
    return data[(data[subjects] >= min_score).all(axis=1)]

def search_by_activities_or_job(data, part_time=False):
    if 'part_time_job' not in data.columns:
        messagebox.showerror("Lỗi", "Dữ liệu không chứa thông tin về công việc làm thêm hoặc hoạt động.")
        return pd.DataFrame()
    return data[data['part_time_job'] == part_time]
