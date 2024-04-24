import requests

params = {
    'worker_id': 1,
    'user_id': 957483050
}

b = requests.post("http://192.168.77.85:8080/updateTelId")
print(b.text)