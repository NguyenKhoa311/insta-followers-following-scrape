import json

# Mở và đọc file JSON
with open('following_response_body.json', 'r') as file:
    data = json.load(file)

# Lấy danh sách người dùng
users = data.get('users', [])  # Sử dụng .get để tránh lỗi nếu không có 'users'

# Trích xuất tên người dùng
user_names = [user['username'] for user in users]

# Ghi danh sách tên người dùng vào file txt
with open('user_names.txt', 'w') as output_file:
    for index, username in enumerate(user_names, start=1):  # Thêm số thứ tự bắt đầu từ 1
        output_file.write(f"{index}. {username}\n")  # Ghi số thứ tự và tên người dùng, mỗi tên một dòng

print("Đã ghi tên người dùng vào file user_names.txt")