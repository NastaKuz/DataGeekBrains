import json
import requests

"""1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
сохранить JSON-вывод в файле *.json."""

url = 'https://api.github.com'
user = 'NastaKuz'

req_json = requests.get(f'{url}/users/{user}/repos').json()

for i in req_json:
    print(i['name'])

with open('githubData.json', 'w') as file:
    json.dump(req_json, file)