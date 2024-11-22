import pandas as pd

# Đọc dữ liệu từ file CSV
file_path = 'student-scores.csv' 
data = pd.read_csv(file_path)

# Chọn 10 cột cần thiết
selected_columns = ['id', 'first_name', 'last_name', 'gender', 'absence_days', 
                    'weekly_self_study_hours', 'career_aspiration', 'math_score', 'history_score', 'english_score'] 
filtered_data = data[selected_columns]

# Xem dữ liệu sau khi lọc
print(filtered_data.head())

# Lưu dữ liệu mới (tùy chọn)
filtered_data.to_csv('filtered_data.csv', index=False)
