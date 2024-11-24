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
        # Đọc dữ liệu hiện có từ file để lấy ID lớn nhất
        data = pd.read_csv(file_path)
        if data.empty: # Kiểm tra file
            current_max_id = 0
        else:
            current_max_id = data['id'].max()

        # ID mới sẽ là ID lớn nhất hiện tại + 1
        new_id = current_max_id + 1

        # Nhập thông tin từ người dùng cho các thuộc tính khác
        full_name = input("Nhập họ và tên: ")
         # Ràng buộc giới tính
        while True:
            gender = input("Nhập giới tính (male/female): ").strip().lower()
            if gender in ['male', 'female']:
                break
            print("Giới tính chỉ được nhập 'male' hoặc 'female'. Vui lòng nhập lại.")

        # Ràng buộc làm thêm (True/False)
        while True:
            part_time_job = input("Có công việc bán thời gian không? (True/False): ").strip().capitalize()
            if part_time_job in ['True', 'False']:
                part_time_job = part_time_job == 'True'  # Chuyển sang kiểu boolean
                break
            print("Chỉ được nhập 'True' hoặc 'False'. Vui lòng nhập lại.")

        # Ràng buộc giá trị >= 0
        def safe_input(prompt):
            while True:
                try:
                    value = float(input(prompt))
                    if 0 <= value <= 100:
                        return value
                    else:
                        print("Bạn phải nhập tương ứng trong đoạn [0-100]. Vui lòng nhập lại.")
                except ValueError:
                    print("Vui lòng nhập một số hợp lệ.")

        weekly_self_study_hours = safe_input("Nhập số giờ tự học hàng tuần (số nguyên): ")
        math_score = safe_input("Nhập điểm Toán (0-100): ")
        history_score = safe_input("Nhập điểm Lịch sử (0-100): ")
        physics_score = safe_input("Nhập điểm Vật lý (0-100): ")
        chemistry_score = safe_input("Nhập điểm Hóa học (0-100): ")
        biology_score = safe_input("Nhập điểm Sinh học (0-100): ")
        english_score = safe_input("Nhập điểm Tiếng Anh (0-100): ")
        geography_score = safe_input("Nhập điểm Địa lý (0-100): ")

        # Tính điểm trung bình của các môn
        scores = [math_score, history_score, physics_score, chemistry_score, biology_score, english_score, geography_score]
        average_score = round(sum(scores) / len(scores), 2)

        # Tạo đối tượng mới dưới dạng dictionary
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

            # Ghi header nếu file chưa có dữ liệu
            if data.empty:
                writer.writeheader()

            # Ghi dòng dữ liệu mới
            writer.writerow(new_record)

        print("Đã thêm đối tượng mới vào file CSV thành công!")

    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")

def delete_data_by_id(file_path):
    """
    Hàm xóa một hoặc nhiều dòng dữ liệu trong file CSV dựa trên ID mà người dùng nhập vào.
    Sau khi xóa, các ID được cập nhật lại.
    """
    try:
        # Đọc dữ liệu từ file CSV
        data = pd.read_csv(file_path)
        
        if data.empty:
            print("File CSV không có dữ liệu để xóa.")
            return
        
        # Yêu cầu nhập ID đến khi đúng định dạng và nằm trong danh sách ID có sẵn
        while True:
            try:
                # Nhập danh sách ID cần xóa
                id_to_delete = input("Nhập các ID cần xóa (phân tách bằng dấu phẩy, ví dụ: 1,2,3): ")
                id_to_delete = [int(id.strip()) for id in id_to_delete.split(',')]

                # Kiểm tra ID có tồn tại trong file không
                if all(id in data['id'].tolist() for id in id_to_delete):
                    break  # Thoát khỏi vòng lặp nếu tất cả ID hợp lệ
                else:
                    print("ID không tồn tại trong file. Vui lòng kiểm tra và nhập lại.")
            except ValueError:
                print("Định dạng không hợp lệ. Vui lòng nhập lại (ví dụ: 1,2,3).")

        # Lọc bỏ các dòng có ID nằm trong danh sách cần xóa
        data = data[~data['id'].isin(id_to_delete)]
        
        # Ghi lại dữ liệu đã xóa vào file CSV
        data.to_csv(file_path, index=False, encoding='utf-8')
        
        print(f"Đã xóa ID: {id_to_delete}. File CSV đã được cập nhật.")
    
    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")

def menu_update(file_path):
    """
    Hàm hiển thị menu để người dùng chọn thao tác.
    """
    while True:
        print("\n==== MENU ====")
        print("1. Thêm đối tượng mới")
        print("2. Xóa đối tượng theo ID")
        print("0. Thoát")
        
        choice = input("Chọn thao tác (1-2-0): ")
        if choice == '1':
            add_new_data(file_path)
        elif choice == '2':
            delete_data_by_id(file_path)
        elif choice == '0':
            print("Thoát chức năng.")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")

