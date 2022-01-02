import requests

url = 'http://localhost:5000/get-category'
arg = {
    'id': 0,
}
r = requests.post(url, json=arg)
print(r.json().get('name'))
