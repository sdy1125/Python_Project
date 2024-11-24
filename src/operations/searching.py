import pandas as pd
from tabulate import tabulate

def search_data(data):
    print("======== TÌM KIẾM ========")
    print("1. Theo tên đầy đủ (Full Name)")
    print("2. Theo ID")
    print("3. Theo điểm tất cả các môn vượt ngưỡng")
    print("4. Theo tham gia hoạt động ngoại khóa hoặc làm thêm")
    print("0. Quay lại menu chính")
    print("=========================")
    
    choice = input("Chọn tiêu chí tìm kiếm: ").strip()
    
    if choice == '1':  # Tìm theo tên đầy đủ
        full_name = input("Nhập tên đầy đủ (hoặc một phần): ").strip()
        result = search_by_full_name(data, full_name)
    elif choice == '2':  # Tìm theo ID
        id_value = input("Nhập ID: ").strip()
        result = search_by_id(data, id_value)
    elif choice == '3':  # Tìm học sinh có điểm tất cả các môn vượt ngưỡng
        try:
            min_score = float(input("Nhập ngưỡng điểm tối thiểu: ").strip())
            result = search_by_all_subjects_score(data, min_score)
        except ValueError:
            print("Ngưỡng điểm phải là một số hợp lệ.")
            return
    elif choice == '4':  # Tìm học sinh tham gia ngoại khóa hoặc làm thêm
        extracurricular = input("Tham gia hoạt động ngoại khóa? (y/n): ").strip().lower() == 'y'
        part_time = input("Làm thêm? (y/n): ").strip().lower() == 'y'
        result = search_by_activities_or_job(data, extracurricular, part_time)
    elif choice == '0':  # Quay lại menu chính
        return
    else:
        print("Lựa chọn không hợp lệ.")
        return
    
    # Hiển thị kết quả tìm kiếm
    if not result.empty:
        print("\nKết quả tìm kiếm:")
        print(tabulate(result, headers="keys", tablefmt="grid", showindex=False))
    else:
        print("\nKhông tìm thấy kết quả nào phù hợp.")

def search_by_id(data, id_value):
    if 'id' not in data.columns:
        print("Cột 'id' không tồn tại trong dữ liệu.")
        return pd.DataFrame()  # Trả về DataFrame rỗng nếu không có cột 'id'
    result = data[data['id'].astype(str).str.lower() == id_value.lower()]
    return result

def search_by_full_name(data, full_name):
    if 'first_name' not in data.columns or 'last_name' not in data.columns:
        print("Dữ liệu không chứa cột 'first_name' hoặc 'last_name'.")
        return pd.DataFrame()
    result = data[data['first_name'].str.contains(full_name, case=False, na=False) |
                  data['last_name'].str.contains(full_name, case=False, na=False)]
    return result

def search_by_all_subjects_score(data, min_score):
    subjects = ['math_score', 'history_score', 'physics_score', 
                'chemistry_score', 'biology_score', 'english_score', 'geography_score']
    missing_subjects = [subject for subject in subjects if subject not in data.columns]
    
    if missing_subjects:
        print(f"Dữ liệu không chứa các cột: {', '.join(missing_subjects)}")
        return pd.DataFrame()
    
    result = data[(data[subjects] >= min_score).all(axis=1)]
    return result

def search_by_activities_or_job(data, extracurricular=False, part_time=False):
    if 'extracurricular_activities' not in data.columns or 'part_time_job' not in data.columns:
        print("Dữ liệu không chứa thông tin về hoạt động ngoại khóa hoặc làm thêm.")
        return pd.DataFrame()
    
    if extracurricular and part_time:
        result = data[(data['extracurricular_activities'] == True) | (data['part_time_job'] == True)]
    elif extracurricular:
        result = data[data['extracurricular_activities'] == True]
    elif part_time:
        result = data[data['part_time_job'] == True]
    else:
        result = pd.DataFrame()
    return result
