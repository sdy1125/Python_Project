from networkx import add_path
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt

# Đọc dữ liệu từ file CSV
file_path = "data/filtered_data.csv"
scores_file_path = "data/student-scores.csv"
data = pd.read_csv(file_path)


# Số lượng dữ liệu trên mỗi trang
rows_per_page = 50

# Chức năng 1: Hiển thị dữ liệu theo dạng bảng với phân trang
def display_table(data, page, rows_per_page):
    total_pages = (len(data) - 1) // rows_per_page + 1
    if page < 1 or page > total_pages:
        print("Số trang không hợp lệ.")
        return
    start_index = (page - 1) * rows_per_page
    end_index = min(start_index + rows_per_page, len(data))
    page_data = data.iloc[start_index:end_index].copy()
    page_data.insert(0, "STT", range(start_index + 1, end_index + 1))
    print("=" * 80)
    print(f"Hiển thị từ dòng {start_index + 1} đến {end_index} trên tổng {len(data)} dữ liệu".center(80))
    print(f"Trang: {page}/{total_pages}".center(80))
    print("=" * 80)
    print(tabulate(page_data, headers="keys", tablefmt="grid", showindex=False))
    print("=" * 80)

# Chức năng phân trang cho chức năng hiển thị
def paginate_data(data, rows_per_page):
    current_page = 1
    total_pages = (len(data) - 1) // rows_per_page + 1
    while True:
        display_table(data, current_page, rows_per_page)
        print("\n* Các lệnh điều khiển *")
        print("n: trang tiếp    p: trang trước")
        print("f: đến trang đầu l: đến trang cuối")
        print("s: đổi số lượng hiển thị mỗi trang")
        print("q: thoát")
        print("-" * 80)
        command = input("Nhập lệnh: ").strip().lower()
        if command == 'n':
            if current_page < total_pages:
                current_page += 1
            else:
                print("Đây là trang cuối.")
        elif command == 'p':
            if current_page > 1:
                current_page -= 1
            else:
                print("Đây là trang đầu.")
        elif command == 'f':
            current_page = 1
        elif command == 'l':
            current_page = total_pages
        elif command == 's':
            try:
                new_rows_per_page = int(input("Nhập số dòng trên mỗi trang: "))
                if new_rows_per_page > 0:
                    rows_per_page = new_rows_per_page
                    total_pages = (len(data) - 1) // rows_per_page + 1
                    current_page = 1  # Quay về trang đầu
                else:
                    print("Số dòng phải lớn hơn 0.")
            except ValueError:
                print("Vui lòng nhập một số hợp lệ.")
        elif command == 'q':
            print("Thoát chức năng hiển thị.")
            break
        else:
            print("Lệnh không hợp lệ. Vui lòng thử lại.")

# Chức năng 2: Sắp xếp dữ liệu
# def sort_data(data):
    
# Chức năng 3: Tìm kiếm dữ liệu
# def search_data(data):
def search_data(data):
    print("========TÌM KIẾM========")
    print("1. Theo tên đầy đủ (Full Name)")
    print("2. Theo giới tính")
    print("3. Theo điểm tất cả các môn vượt ngưỡng")
    print("4. Theo tham gia hoạt động ngoại khóa hoặc làm thêm")
    print("0. Quay lại menu chính")
    print("========================")
    
    choice = input("Chọn tiêu chí tìm kiếm: ").strip()
    
    if choice == '1':  # Tìm theo tên đầy đủ
        full_name = input("Nhập tên đầy đủ (hoặc một phần): ").strip()
        result = search_by_full_name(data, full_name)
    elif choice == '2':  # Tìm theo giới tính
        gender = input("Nhập giới tính (male/female): ").strip()
        result = search_by_gender(data, gender)
    elif choice == '3':  # Tìm học sinh có điểm tất cả các môn vượt ngưỡng
        min_score = int(input("Nhập ngưỡng điểm tối thiểu: ").strip())
        result = search_by_all_subjects_score(data, min_score)
    elif choice == '4':  # Tìm học sinh tham gia ngoại khóa hoặc làm thêm
        extracurricular = input("Tham gia hoạt động ngoại khóa? (y/n): ").strip().lower() == 'y'
        part_time = input("Làm thêm? (y/n): ").strip().lower() == 'y'
        result = search_by_activities_or_job(data, extracurricular, part_time)
    elif choice == '0':  # Thoát menu
        return
    else:
        print("Lựa chọn không hợp lệ.")
        return
    
    # Hiển thị kết quả tìm kiếm
    if not result.empty:
        print("Kết quả tìm kiếm:")
        print(tabulate(result, headers="keys", tablefmt="grid", showindex=False))
    else:
        print("Không tìm thấy kết quả nào.")
def search_by_gender(data, gender):
    if gender.lower() not in ['male', 'female']:
        print("Giới tính không hợp lệ. Vui lòng nhập 'male' hoặc 'female'.")
        return pd.DataFrame()  # Trả về DataFrame rỗng nếu giới tính không hợp lệ
    result = data[data['gender'].str.lower() == gender.lower()]
    return result
def search_by_full_name(data, full_name):
    result = data[data['first_name'].str.contains(full_name, case=False, na=False) |
                  data['last_name'].str.contains(full_name, case=False, na=False)]
    return result
def search_by_all_subjects_score(data, min_score):
    subjects = ['math_score', 'history_score', 'physics_score', 
                'chemistry_score', 'biology_score', 'english_score', 'geography_score']
    result = data[(data[subjects] >= min_score).all(axis=1)]
    return result
def search_by_activities_or_job(data, extracurricular=False, part_time=False):
    if extracurricular and part_time:
        result = data[(data['extracurricular_activities'] == True) | (data['part_time_job'] == True)]
    elif extracurricular:
        result = data[data['extracurricular_activities'] == True]
    elif part_time:
        result = data[data['part_time_job'] == True]
    else:
        result = data
    return result



# Chức năng 4: Thêm dữ liệu
# def add_data(data):

# Chức năng 5: Cập nhật dữ liệu
# def update_data(data):


# Chức năng 6: Xóa dữ liệu
# def delete_data(data):


# Chức năng 7: Hiển thị biểu đồ
# def plot_data(data):
def plot_data():
    try:
        # Chỉ đọc dữ liệu từ file khi chọn chức năng số 7
        scores_data = pd.read_csv(scores_file_path)
        print(f"Dữ liệu đã được tải từ {scores_file_path}")
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file {scores_file_path}.")
        return

    while True:
        print("\n======== BIỂU ĐỒ ========")
        print("1. Số lượng học sinh theo giới tính")
        print("2. Điểm trung bình của các môn học")
        print("0. Quay lại menu chính")
        print("=========================")
        
        choice = input("Chọn biểu đồ bạn muốn vẽ: ").strip()
        
        if choice == '1':  # Biểu đồ số lượng học sinh theo giới tính
            if 'gender' not in scores_data.columns:
                print("Dữ liệu không chứa thông tin về giới tính.")
                continue
            
            gender_counts = scores_data['gender'].str.lower().value_counts()
            gender_counts.plot(kind='bar', color=['#1f77b4', '#ff7f0e'], alpha=0.8, edgecolor='black')
            plt.title('Số lượng học sinh theo giới tính', fontsize=14)
            plt.xlabel('Giới tính', fontsize=12)
            plt.ylabel('Số lượng', fontsize=12)
            plt.xticks(rotation=0, fontsize=10)
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.show()
        
        elif choice == '2':  # Biểu đồ điểm trung bình các môn học
            all_subjects = [
                'math_score', 'history_score', 'physics_score', 
                'chemistry_score', 'biology_score', 'english_score', 'geography_score'
            ]
            
            available_subjects = [subject for subject in all_subjects if subject in scores_data.columns]
            if not available_subjects:
                print("Không có cột môn học hợp lệ trong dữ liệu.")
                continue
            
            average_scores = scores_data[available_subjects].mean()
            average_scores.plot(kind='bar', color='#76c7c0', alpha=0.8, edgecolor='black')
            plt.title('Điểm trung bình của các môn học', fontsize=14)
            plt.xlabel('Môn học', fontsize=12)
            plt.ylabel('Điểm trung bình', fontsize=12)
            plt.xticks(rotation=45, fontsize=10)
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.show()
        
        elif choice == '0':  # Thoát menu
            print("Quay lại menu chính.")
            break
        
        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")


def main():
    global data
    while True:
        print("========MENU========")
        print("1. Hiển thị danh sách dữ liệu")
        print("2. Sắp xếp dữ liệu")
        print("3. Tìm kiếm dữ liệu")
        print("4. Thêm dữ liệu")
        print("5. Cập nhật dữ liệu được chọn")
        print("6. Xóa dữ liệu")
        print("7. Hiển thị biểu đồ")
        print("0. Thoát chương trình")
        print("====================")
        
        choice = input("Nhập lựa chọn: ").strip()
        
        if choice == '1':
            paginate_data(data, rows_per_page)
        elif choice == '2':
            sort_data(data)
        elif choice == '3':
            search_data(data)
        elif choice == '4':
            data = add_path(data)
        elif choice == '5':
            data = update_data(data)
        elif choice == '6':
            data = delete_data(data)
        elif choice == '7':
            plot_data()
        elif choice == '0':
            print("Thoát chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")

if __name__ == "__main__":
    main()
