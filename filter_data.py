import pandas as pd 

# Đọc dữ liệu từ file CSV
file_path = 'data/student-scores.csv' 
data = pd.read_csv(file_path)

# Tạo cột 'full_name' bằng cách ghép cột 'first_name' và 'last_name'
data['full_name'] = data['first_name'] + ' ' + data['last_name']

# Tạo cột 'average_score' để tính điểm trung bình
data['average_score'] = data[['math_score', 'history_score', 'english_score']].mean(axis=1)

# Làm tròn giá trị trong cột 'average_score' thành 2 chữ số thập phân
data['average_score'] = data['average_score'].round(2)

# Chọn 11 cột cần thiết (thêm 'average_score')
selected_columns = ['id', 'full_name', 'gender', 'part_time_job', 
                    'weekly_self_study_hours', 
                    'math_score','history_score','physics_score',
                    'chemistry_score','biology_score','english_score',
                    'geography_score','average_score'] 
filtered_data = data[selected_columns]

#Xuất thông báo
print("Đã tạo file csv được lọc.")

# Lưu dữ liệu mới (tùy chọn)
filtered_data.to_csv('data/filtered_data.csv', index=False)