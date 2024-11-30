import tkinter as tk
from tkinter import messagebox, simpledialog
import pandas as pd
import csv
from src.display.table_display import create_table_window

def add_new_data(file_path):
    """
    Thêm một đối tượng mới vào file CSV:
    - ID tự động cập nhật dựa trên giá trị ID lớn nhất hiện có trong file.
    - Người dùng nhập đúng định dạng các thuộc tính.
    - Ghi đối tượng mới vào cuối file.
    """
    try:
        # Đọc dữ liệu hiện có từ file
        data = pd.read_csv(file_path)
        if data.empty:
            current_max_id = 0
        else:
            current_max_id = data['id'].max()
        new_id = current_max_id + 1  # ID mới sẽ là ID lớn nhất hiện tại + 1

        # Tạo cửa sổ nhập liệu mới
        def submit_data(entry_full_name, entry_gender, entry_part_time_job, entry_weekly_self_study_hours, entries):
            try:
                # Lấy dữ liệu từ các ô nhập liệu
                full_name = entry_full_name.get()
                gender = entry_gender.get().strip().lower()
                part_time_job = entry_part_time_job.get().strip().capitalize()
                weekly_self_study_hours = float(entry_weekly_self_study_hours.get())
                
                # Lấy điểm từ các môn học
                subjects = ["Toán", "Lịch Sử", "Vật Lý", "Hóa Học", "Sinh Học", "Tiếng Anh", "Địa Lý"]
                scores = {}
                
                for subject in subjects:
                    score = float(entries[subject].get())
                    if score < 0 or score > 100:
                        messagebox.showerror("Lỗi", f"Điểm {subject} phải nằm trong khoảng từ 0 đến 100.")
                        return
                    scores[subject] = score
                
                math_score = scores["Toán"]
                history_score = scores["Lịch Sử"]
                physics_score = scores["Vật Lý"]
                chemistry_score = scores["Hóa Học"]
                biology_score = scores["Sinh Học"]
                english_score = scores["Tiếng Anh"]
                geography_score = scores["Địa Lý"]
                
                # Kiểm tra giới tính hợp lệ
                if gender not in ['male', 'female']:
                    messagebox.showerror("Lỗi", "Giới tính phải là 'male' hoặc 'female'.")
                    return

                # Kiểm tra làm thêm (True/False)
                if part_time_job not in ['True', 'False']:
                    messagebox.showerror("Lỗi", "Làm thêm phải là 'True' hoặc 'False'.")
                    return
                
                part_time_job = part_time_job == 'True'  # Chuyển sang kiểu boolean

                # Tính điểm trung bình của các môn
                scores_list = [math_score, history_score, physics_score, chemistry_score, biology_score, english_score, geography_score]
                average_score = round(sum(scores_list) / len(scores_list), 2)

                # Tạo dòng dữ liệu mới
                new_record = {
                    "id": new_id,
                    "full_name": full_name,
                    "gender": gender,
                    "part_time_job": part_time_job,
                    "weekly_self_study_hours": weekly_self_study_hours,
                    "math_score": math_score,
                    "history_score": history_score,
                    "physics_score": physics_score,
                    "chemistry_score": chemistry_score,
                    "biology_score": biology_score,
                    "english_score": english_score,
                    "geography_score": geography_score,
                    "average_score": average_score,
                }

                # Ghi đối tượng mới vào file CSV
                with open(file_path, mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=new_record.keys())
                    if data.empty:
                        writer.writeheader()  # Ghi header nếu file chưa có dữ liệu
                    writer.writerow(new_record)  # Ghi dòng dữ liệu mới
                
                messagebox.showinfo("Thành công", f"Đã thêm đối tượng mới vào file CSV với ID {new_id}")
                display_data_update(file_path)
                new_data_window.destroy()  # Đóng cửa sổ sau khi thêm thành công
            except ValueError as e:
                messagebox.showerror("Lỗi", "Vui lòng nhập đúng định dạng dữ liệu. Lỗi: " + str(e))


        # Tạo cửa sổ nhập liệu mới
        new_data_window = tk.Toplevel()
        new_data_window.title("Thêm Dữ Liệu")

        # Tạo các Label và Entry cho từng trường
        tk.Label(new_data_window, text="Họ và tên:").grid(row=0, column=0, padx=10, pady=5)
        entry_full_name = tk.Entry(new_data_window)
        entry_full_name.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(new_data_window, text="Giới tính (male/female):").grid(row=1, column=0, padx=10, pady=5)
        entry_gender = tk.Entry(new_data_window)
        entry_gender.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(new_data_window, text="Làm thêm (True/False):").grid(row=2, column=0, padx=10, pady=5)
        entry_part_time_job = tk.Entry(new_data_window)
        entry_part_time_job.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(new_data_window, text="Số giờ tự học hàng tuần:").grid(row=3, column=0, padx=10, pady=5)
        entry_weekly_self_study_hours = tk.Entry(new_data_window)
        entry_weekly_self_study_hours.grid(row=3, column=1, padx=10, pady=5)

        # Các trường điểm cho các môn học
        subjects = ["Toán", "Lịch Sử", "Vật Lý", "Hóa Học", "Sinh Học", "Tiếng Anh", "Địa Lý"]
        entries = {}
        for idx, subject in enumerate(subjects, 4):
            tk.Label(new_data_window, text=f"Điểm {subject}:").grid(row=idx, column=0, padx=10, pady=5)
            entries[subject] = tk.Entry(new_data_window)
            entries[subject].grid(row=idx, column=1, padx=10, pady=5)

        # Nút gửi thông tin
        submit_button = tk.Button(new_data_window, text="Thêm Dữ Liệu", command=lambda: submit_data(entry_full_name, entry_gender, entry_part_time_job, entry_weekly_self_study_hours, entries))
        submit_button.grid(row=len(subjects) + 4, column=0, columnspan=2, pady=20)

        new_data_window.mainloop()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")

def delete_data_by_id_gui(file_path):
    """
    Hàm xóa một hoặc nhiều dòng dữ liệu trong file CSV dựa trên ID mà người dùng nhập vào.
    Sau khi xóa, các ID được cập nhật lại.
    """
    try:
        data = pd.read_csv(file_path) # Đọc dữ liệu từ file CSV
        if data.empty:
            messagebox.showinfo("Thông báo", "File CSV không có dữ liệu để xóa.")
            return
        
        # Yêu cầu nhập ID đến khi đúng định dạng và nằm trong danh sách ID có sẵn
        while True:
            # Yêu cầu người dùng nhập ID
            id_to_delete = simpledialog.askstring("Xóa dữ liệu", "Nhập các ID cần xóa (phân tách bằng dấu phẩy):")
            if not id_to_delete:
                return  # Thoát nếu người dùng nhấn hủy

            try:
                # Chuyển danh sách ID thành danh sách số nguyên
                id_to_delete = [int(id.strip()) for id in id_to_delete.split(',')]

                # Kiểm tra nếu tất cả ID có trong file
                if all(id in data['id'].tolist() for id in id_to_delete):
                    # Lọc dữ liệu và lưu lại
                    data = data[~data['id'].isin(id_to_delete)]
                    data.to_csv(file_path, index=False, encoding='utf-8')
                    messagebox.showinfo("Thành công", f"Đã xóa ID: {id_to_delete}.")
                    display_data_update(file_path)
                    break  # Thoát vòng lặp khi hoàn tất
                else:
                    messagebox.showerror("Lỗi", "Một hoặc nhiều ID không tồn tại trong file. Vui lòng nhập lại.")
            except ValueError:
                messagebox.showerror("Lỗi", "Định dạng ID không hợp lệ. Vui lòng nhập lại.")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")

def display_data_update(file_path):
   data = pd.read_csv(file_path)
   create_table_window(data, rows_per_page=50)

# Giao diện chính
def menu_update(file_path):
    root = tk.Tk()
    root.title("Thêm/Xóa dữ liệu")
    root.geometry("300x150")
    root.config(bg='black')

    tk.Button(root, text="Thêm đối tượng mới", command=lambda: add_new_data(file_path), width=20).pack(pady=10)
    tk.Button(root, text="Xóa đối tượng theo ID", command=lambda: delete_data_by_id_gui(file_path), width=20).pack(pady=10)
    tk.Button(root, text="Thoát", command=root.destroy).pack(pady=10)
    root.mainloop()
