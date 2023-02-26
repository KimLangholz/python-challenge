import requests
import logging
from typing import Dict, Optional, Any


def make_get_request(url: str) -> Optional[requests.Response]:
    """
    Send a GET request to the specified URL and return the response object.

    Args:
        url (str): The URL to send the request to.

    Returns:
        Optional[requests.Response]: The response object if the request was successful, 
        otherwise None.
    """
    with requests.Session() as session:
        try:
            response = session.get(url)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as err:
            logging.error(f"Request error: {err}")
            return None

def get_user_data(username: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve the user data for the specified username.

    Args:
        username (str): The username of the user to retrieve data for.

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing the user data if the request was successful, 
        otherwise None.
    """
    endpoint = f"https://d16m5wbro86fg2.cloudfront.net/api/user/by-username/{username}"
    response = make_get_request(endpoint)
    if response is not None:
        return response.json()
    else:
        return None

def get_lego_sets() -> Dict[str, Any]:
    """
    Retrieve a list of Lego sets from the web service.

    Returns:
        Dict[str, Any]: A dictionary containing information about Lego sets.
    """
    endpoint = "https://d16m5wbro86fg2.cloudfront.net/api/sets"
    response = make_get_request(endpoint)
    if response is not None:
        return response.json()
    else:
        return None

def get_user_inventory_details(user_data) -> Dict[str, Any]:
    """
    Retrieve the user's Lego inventory details.

    Args:
        user_data (Dict[str, Any]): A dictionary containing the user data.

    Returns:
        Dict[str, Any]: A dictionary containing information about the user's Lego inventory.
    """
    endpoint = f"https://d16m5wbro86fg2.cloudfront.net/api/user/by-id/{user_data['id']}"
    response = make_get_request(endpoint)
    if response is not None:
        return response.json()
    else:
        return None

def get_lego_set_details(lego_set_id: str) -> Dict:
    """
    Retrieve the details of the specified Lego set.

    Args:
        lego_set_id (str): The ID of the Lego set to retrieve details for.

    Returns:
        Dict: A dictionary containing details about the Lego set.
    """
    endpoint = f"https://d16m5wbro86fg2.cloudfront.net/api/set/by-id/{lego_set_id}"
    response = make_get_request(endpoint)
    if response is not None:
        return response.json()
    else:
        return None

