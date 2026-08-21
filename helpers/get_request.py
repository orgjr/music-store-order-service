import requests


def get_request(url: str, params: None) -> dict:
    if params:
        response = requests.get(f"{url}/{params}/", timeout=5)
    else:
        response = requests.get(url, timeout=5)
    response.raise_for_status()
    data = response.json()
    return data
