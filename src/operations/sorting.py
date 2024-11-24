from src.display.pagination import paginate_data

def sort_data(data,rows_per_page):
    """
    Thực hiện sắp xếp dữ liệu theo các tiêu chí, hiển thị kết quả ngay sau khi sắp xếp
    và cho phép phân trang (tái sử dụng phân trang).
    """
    while True:
        print("\n======== MENU SẮP XẾP ========")
        print("1. Sắp xếp theo giờ học cuối tuần (weekly_self_study_hours)")
        print("2. Sắp xếp theo điểm trung bình (average_score)")

        print("0. Quay lại menu chính")
        print("==============================")
        column_choice = input("Nhập lựa chọn: ").strip()

        if column_choice == '0':
            print("Quay lại menu chính.")
            return data  # Giữ trạng thái hiện tại của dữ liệu

    
        if column_choice == '1':
            column_name = 'weekly_self_study_hours'
        elif column_choice == '2':
            column_name = 'average_score'
        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")
            continue  # Quay lại menu sắp xếp

        # Hỏi người dùng sắp xếp tăng dần hay giảm dần
        ascending_choice = input("\nSắp xếp tăng dần? (y/n): ").strip().lower()
        if ascending_choice not in ['y', 'n']:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")
            continue  # Quay lại menu sắp xếp

        ascending = ascending_choice == 'y'

        # Sắp xếp dữ liệu
        sorted_data = data.sort_values(by=column_name, ascending=ascending)
        print(f"\nDữ liệu đã được sắp xếp theo cột '{column_name}' ({'tăng dần' if ascending else 'giảm dần'}).")

        # Tái sử dụng phân trang để hiển thị dữ liệu đã sắp xếp
        paginate_data(sorted_data,rows_per_page)

        # Sau khi phân trang xong, quay lại menu sắp xếp
        print("\nQuay lại menu sắp xếp...")