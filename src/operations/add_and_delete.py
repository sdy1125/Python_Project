import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import pandas as pd
import csv



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
        new_id = current_max_id + 1 # ID mới sẽ là ID lớn nhất hiện tại + 1

        # Lấy dữ liệu từ người dùng qua hộp thoại
        full_name = simpledialog.askstring("Thêm dữ liệu", "Nhập họ và tên:")
        if not full_name:
            return
        
        # Ràng buộc giới tính
        while True:
            gender = simpledialog.askstring("Thêm dữ liệu", "Nhập giới tính (male/female):").strip().lower()
            if gender in ['male', 'female']:
                break
            messagebox.showerror("Lỗi", "Giới tính chỉ được nhập 'male' hoặc 'female'.")

        # Ràng buộc làm thêm (True/False)
        while True:
            part_time_job = simpledialog.askstring("Thêm dữ liệu", "Có làm thêm không? (True/False):").strip().capitalize()
            if part_time_job in ['True', 'False']:
                part_time_job = part_time_job == 'True'  # Chuyển sang kiểu boolean
                break
            messagebox.showerror("Lỗi", "Chỉ được nhập 'True' hoặc 'False'.")

        # Hàm nhập an toàn giá trị
        def safe_input(prompt):
            while True:
                try:
                    value = float(simpledialog.askstring("Thêm dữ liệu", prompt))
                    if 0 <= value <= 100:
                        return value
                    else:
                        messagebox.showerror("Lỗi", "Giá trị phải từ 0 đến 100.")
                except ValueError:
                    messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ.")

        weekly_self_study_hours = safe_input("Nhập số giờ tự học hàng tuần:")
        math_score = safe_input("Nhập điểm Toán (0-100):")
        history_score = safe_input("Nhập điểm Lịch sử (0-100):")
        physics_score = safe_input("Nhập điểm Vật lý (0-100):")
        chemistry_score = safe_input("Nhập điểm Hóa học (0-100):")
        biology_score = safe_input("Nhập điểm Sinh học (0-100):")
        english_score = safe_input("Nhập điểm Tiếng Anh (0-100):")
        geography_score = safe_input("Nhập điểm Địa lý (0-100):")

        # Tính điểm trung bình của các môn
        scores = [math_score, history_score, physics_score, chemistry_score, biology_score, english_score, geography_score]
        average_score = round(sum(scores) / len(scores), 2)

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
                writer.writeheader() # Ghi header nếu file chưa có dữ liệu
            writer.writerow(new_record) # Ghi dòng dữ liệu mới
        messagebox.showinfo("Thành công", "Đã thêm đối tượng mới vào file CSV.")
        display_data_update(file_path)
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
