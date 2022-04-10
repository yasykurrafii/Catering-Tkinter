import requests
import json

def build_json(file):
    return json.loads(file)

def fetch_api(url):
    response = requests.get(url).text
    json_ = build_json(response)
    return json_