import requests, json
from typing import Dict

def call_api(url: str) -> Dict:
    """
    Calls a web API at the given URL and returns the JSON response as a dictionary.

    Args:
        url (str): The URL of the API to call.

    Returns:
        Dict: A dictionary containing the JSON response from the API. If the API returns a non-200 HTTP status code, 
        returns None instead.
    """
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.content)
        return data
    else:
        return None