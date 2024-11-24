import pandas as pd
def update_data_by_id(data, file_path):
    """
    Cập nhật toàn bộ dữ liệu thuộc hàng có ID được chọn.
    :param data: DataFrame chứa dữ liệu
    :param file_path: Đường dẫn file CSV để lưu thay đổi
    :return: DataFrame đã cập nhật
    """
    id_column = "id"  # Mặc định cột ID là "ID"

    if id_column not in data.columns:
        print(f"Cột '{id_column}' không tồn tại trong dữ liệu.")
        return data

    # Nhập ID cần tìm
    search_id = input(f"Nhập giá trị ID để cập nhật: ").strip()
    try:
        # Chuyển ID về kiểu số nếu dữ liệu ID là số
        search_id = int(search_id) if data[id_column].dtype in ['int64', 'float64'] else search_id
    except ValueError:
        print("ID không hợp lệ. Vui lòng nhập đúng định dạng.")
        return data

    # Lấy dòng tương ứng với ID
    matching_rows = data[data[id_column] == search_id]

    if matching_rows.empty:
        print(f"Không tìm thấy dữ liệu với ID = {search_id}.")
        return data

    # Lấy chỉ số của dòng cần cập nhật
    row_index = matching_rows.index[0]
    print("\nThông tin hiện tại của dòng được chọn:")
    print(matching_rows.iloc[0])  # Hiển thị dòng dữ liệu

    # Cập nhật từng trường dữ liệu
    for column in data.columns:
        if column == id_column:
            continue  # Không cho phép thay đổi cột ID
        current_value = data.at[row_index, column]
        new_value = input(f"Nhập giá trị mới cho '{column}' (hiện tại: {current_value}, nhấn Enter để giữ nguyên): ").strip()
        
        if new_value:  # Nếu có thay đổi
            try:
                # Chuyển đổi kiểu dữ liệu nếu cần
                if pd.api.types.is_numeric_dtype(data[column]):
                    new_value = float(new_value) if '.' in new_value else int(new_value)
                data.at[row_index, column] = new_value
                print(f"Đã cập nhật '{column}' thành '{new_value}'.")
            except ValueError:
                print(f"Giá trị không hợp lệ cho cột '{column}'. Giữ nguyên giá trị cũ.")

    # Lưu thay đổi vào file CSV
    save_choice = input("\nBạn có muốn lưu thay đổi vào file không? (y/n): ").strip().lower()
    if save_choice == 'y':
        data.to_csv(file_path, index=False)
        print(f"Dữ liệu đã được lưu vào '{file_path}'.")
    else:
        print("Thay đổi chỉ được áp dụng trong phiên làm việc hiện tại.")

    print("Cập nhật dữ liệu hoàn tất.")
    return data