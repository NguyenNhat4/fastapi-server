import requests

# Giả sử đây là dữ liệu bạn nhận được từ bước đăng nhập
login_response = {'access_token': 'johndoe', 'token_type': 'bearer'}
token = login_response['access_token']

# Cấu hình Header với Bearer Token
headers = {
    "Authorization": f"Bearer {token}"
}

# Gửi yêu cầu đến một route yêu cầu xác thực (ví dụ: /users/me)
protected_url = "http://127.0.0.1:8000/users/me"
response = requests.get(protected_url, headers=headers)

print(response.json())
