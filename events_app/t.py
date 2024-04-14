import requests


url = "http://127.0.0.1:8000/api/v1/cities/4/"
data = {'city_name': 'Владимир 30'}
headers = {'Content-type': 'application/json'}

response = requests.put(url, json=data, headers=headers)

print(response.json())