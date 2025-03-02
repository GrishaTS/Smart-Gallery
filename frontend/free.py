import requests

url = "http://localhost:8000/images/"
files = {"files": ("test.jpg", open("C:/Users/bezgr/STUDY/HSE/Course 2/Smart-Gallery/frontend/test.jpg", "rb"), "image/jpeg")}
response = requests.post(url, files=files)

# Выведем полный ответ сервера
print("Status Code:", response.status_code)
print("Response Text:", response.text)  # Посмотрим, что вернул сервер
