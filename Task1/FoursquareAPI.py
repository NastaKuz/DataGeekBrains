import json
import requests

"""Foursquare:"""

params = {
        "client_id": "O3VIOCNVZJFUEBGA33RIBBTJY4MBHYD4KVS4ZCOXKZ3S0KM5",
        "client_secret": "KLUIRIILFRV4RHBS2QWZA0ELYU2M5L20TKEE0UI1ZS4RLHMX",
        "v": "20210308",
        "ll": "55.76060644163612, 37.61892475828963",
        "query": "museum",
        "limit": 1
    }
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  "Chrome/92.0.4515.107 Safari/537.36"
}

req_json = requests.get(
    "https://api.foursquare.com/v2/venues/explore",
    headers=headers,
    params=params
    ).json()

first_result = req_json['response']['groups'][0]['items'][0]['venue']

print(first_result['name'], "по адресу", first_result['location']['address'])

with open('foursquareData.json', 'w') as file:
    json.dump(req_json, file)