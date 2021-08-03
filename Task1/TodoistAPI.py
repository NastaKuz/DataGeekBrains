import json
import requests

"""2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis). Найти среди них любое, требующее
авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

Todoist:
"""

auth = '3b26e74302c5186ca63895fcf15c79d097c99886'

headers = {
        "Authorization": f"Bearer {auth}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      "Chrome/92.0.4515.107 Safari/537.36"
    }
req_json = requests.get(
    "https://api.todoist.com/rest/v1/projects",
    headers=headers).json()

for i in req_json:
    print(i['name'])

with open('todoistData.json', 'w') as file:
    json.dump(req_json, file)
