import requests
import logging
from typing import Dict, Optional, Any

def make_request(url: str) -> Optional[requests.Response]:
    with requests.Session() as session:
        try:
            response = session.get(url)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as err:
            logging.error(f"Request error: {err}")
            return None

def get_user_data(username: str) -> Optional[Dict[str, Any]]:
    
    endpoint = f"https://d16m5wbro86fg2.cloudfront.net/api/user/by-username/{username}"
    response = make_request(endpoint)
    if response is not None:
        return response.json()
    else:
        return None

def get_lego_sets() -> Dict[str, Any]:
    endpoint = "https://d16m5wbro86fg2.cloudfront.net/api/sets"
    response = make_request(endpoint)
    if response is not None:
        return response.json()
    else:
        return None

def get_user_inventory_details(user_data) -> Dict[str, Any]:
    endpoint = f"https://d16m5wbro86fg2.cloudfront.net/api/user/by-id/{user_data['id']}"
    response = make_request(endpoint)
    if response is not None:
        return response.json()
    else:
        return None

def get_lego_set_details(lego_set_id: str) -> Dict:
    endpoint = f"https://d16m5wbro86fg2.cloudfront.net/api/set/by-id/{lego_set_id}"
    response = make_request(endpoint)
    if response is not None:
        return response.json()
    else:
        return None

