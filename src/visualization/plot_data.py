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
    gender_counts = data['gender'].str.lower().value_counts()
    gender_counts.plot(kind='bar', color=['#1f77b4', '#ff7f0e'], alpha=0.8, edgecolor='black')
    plt.title('Số lượng học sinh theo giới tính', fontsize=14)
    plt.xlabel('Giới tính', fontsize=12)
    plt.ylabel('Số lượng', fontsize=12)
    plt.xticks(rotation=0, fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
def show_chart3(data):  
    all_subjects = ['math_score', 'history_score', 'physics_score', 
                    'chemistry_score', 'biology_score', 'english_score', 'geography_score']
            
    available_subjects = [subject for subject in all_subjects if subject in data.columns]
    average_scores = data[available_subjects].mean()
    average_scores.plot(kind='bar', color='#76c7c0', alpha=0.8, edgecolor='black')
    plt.title('Điểm trung bình của các môn học', fontsize=14)
    plt.xlabel('Môn học', fontsize=12)
    plt.ylabel('Điểm trung bình', fontsize=12)
    plt.xticks(rotation=45, fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# Giao diện chính
def menu_display_plot_data(data):
    root = tk.Tk()
    root.title("Thêm/Xóa dữ liệu")
    tk.Button(root, text="Phân bố điểm trung bình của học sinh", command=lambda: show_chart1(data)).pack(pady=10)
    tk.Button(root, text="Số lượng học sinh theo giới tính", command=lambda: show_chart2(data)).pack(pady=10)
    tk.Button(root, text="Điểm trung bình của các môn học", command=lambda: show_chart3(data)).pack(pady=10)
    tk.Button(root, text="Thoát", command=root.destroy).pack(pady=10)
    root.mainloop()