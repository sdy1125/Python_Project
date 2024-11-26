import tkinter as tk
from tkinter import ttk
from matplotlib import pyplot as plt
import pandas as pd

def show_chart1(data):
    # Chia điểm trung bình thành 5 phần hợp lý
    bins = [48, 60, 70, 80, 90, 100]  # Khoảng chia
    labels = ['48-60', '60-70', '70-80', '80-90', '90-100']  # Nhãn cho mỗi phần
    data['Score Range'] = pd.cut(data['average_score'], bins=bins, labels=labels, right=False)

    # Đếm số lượng học sinh trong mỗi phần
    score_distribution = data['Score Range'].value_counts(sort=False)

    # Vẽ biểu đồ cột (bar chart) 
    plt.figure(figsize=(8, 6))
    plt.bar(score_distribution.index.astype(str), score_distribution.values, color='skyblue', edgecolor='purple')

    # Thêm tiêu đề và nhãn trục
    plt.title("Phân bố điểm trung bình của học sinh", fontsize=14)
    plt.xlabel("Điểm trung bình", fontsize=12)
    plt.ylabel("Số lượng học sinh", fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)

    # Hiển thị biểu đồ
    plt.tight_layout()
    plt.show()
def show_chart2(data):        
    all_subjects = ['math_score', 'history_score', 'physics_score', 
                    'chemistry_score', 'biology_score', 'english_score', 'geography_score']

    df_above_80 = data[data[all_subjects].gt(80).any(axis=1)] 
    part_time_count = df_above_80[df_above_80['part_time_job'] == 1].shape[0] 
    no_part_time_count = df_above_80[df_above_80['part_time_job'] == 0].shape[0] 
    categories = ['Có làm thêm', 'Không làm thêm']
    counts = [part_time_count, no_part_time_count]
    plt.figure(figsize=(8, 8))
    plt.pie(counts, labels=categories, autopct='%1.1f%%', startangle=140, colors=['green', 'blue'])
    plt.title('Số lượng sinh viên có điểm trên 80 và có/không có việc làm thêm')
    plt.show()

def show_chart3(data):  
    all_subjects = ['math_score', 'history_score', 'physics_score', 
                    'chemistry_score', 'biology_score', 'english_score', 'geography_score']
    students_above_80 = []
    for subject in all_subjects:
        count_above_80 = (data[subject] > 80).sum()
        students_above_80.append(count_above_80)
    
    # Plot the pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(students_above_80, labels=all_subjects, autopct='%1.1f%%', startangle=140)
    plt.title('Số lượng học sinh có điểm trên 80 của từng môn học')
    plt.show()

# Giao diện chính
def menu_display_plot_data(data):
    root = tk.Tk()
    root.title("Đồ thị trực quan")
    root.geometry("300x200")
    root.config(bg='black')
    
    tk.Button(root, text="Phân bố điểm trung bình của học sinh", command=lambda: show_chart1(data), width=34).pack(pady=10)
    tk.Button(root, text="Biểu đồ phân bố điểm dựa trên việc làm thêm", command=lambda: show_chart2(data), width=34).pack(pady=10)
    tk.Button(root, text="Phân bố số lượng học sinh có điểm trên 80", command=lambda: show_chart3(data), width=34).pack(pady=10)
    tk.Button(root, text="Thoát", command=root.destroy).pack(pady=10)
    root.mainloop()
