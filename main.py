from flask import Flask
from flask_restful import Api, Resource
from cachetools import TTLCache
import requests
import logging
from typing import Dict, Any
from helpers.api_functions import *
from helpers.functions import find_buildable_sets
from helpers.functions import find_sets_with_less_bricks_than_users_inventory
from helpers.functions import sort_user_inventory

app = Flask(__name__)
api = Api(app)


class BuildableSetsFromCurrentInventory(Resource):
    logging.basicConfig(level=logging.DEBUG)
    cache = TTLCache(maxsize=1000, ttl=180)

    def get(self, username: str) -> Dict[str, Any]:
        try:
            if username not in self.cache:
                self.cache[username] = get_user_data(username)

            user_data = self.cache[username]

            lego_sets: Dict[str, Any] = get_lego_sets()

            sets_buildable_with_users_lego_count: Dict[str, str] = find_sets_with_less_bricks_than_users_inventory(
                lego_sets, user_data['brickCount'])

            if not sets_buildable_with_users_lego_count:
                return {"message": "No buildable sets found."}

            users_inventory: Dict[str, Any] = sort_user_inventory(
                get_user_inventory_details(user_data))

            buildable_sets: Dict[str, Dict[str, str]] = find_buildable_sets(users_inventory, lego_sets, False)

            return {"buildable_sets": buildable_sets}


        except requests.exceptions.HTTPError as err:
            logging.error(f"Request error: {err}")
            return {"message": "An error occurred while retrieving user data."}

        except Exception as err:
            logging.error(f"An error occurred: {err}")
            return {"message": "An error occurred."}

class BuildableSetsWithColorFlexibility(Resource):
    logging.basicConfig(level=logging.DEBUG)
    cache = TTLCache(maxsize=1000, ttl=180)

    def get(self, username: str) -> Dict[str, Any]:
        try:
            if username not in self.cache:
                self.cache[username] = get_user_data(username)

            user_data = self.cache[username]

            lego_sets: Dict[str, Any] = get_lego_sets()

            sets_buildable_with_users_lego_count: Dict[str, str] = find_sets_with_less_bricks_than_users_inventory(
                lego_sets, user_data['brickCount'])

            if not sets_buildable_with_users_lego_count:
                return {"message": "No buildable sets found."}

            users_inventory: Dict[str, Any] = sort_user_inventory(
                get_user_inventory_details(user_data))

            buildable_sets: Dict[str, Dict[str, str]] = find_buildable_sets(users_inventory, lego_sets, True)

            return {"buildable_sets": buildable_sets}


        except requests.exceptions.HTTPError as err:
            logging.error(f"Request error: {err}")
            return {"message": "An error occurred while retrieving user data."}

        except Exception as err:
            logging.error(f"An error occurred: {err}")
            return {"message": "An error occurred."}

api.add_resource(BuildableSetsFromCurrentInventory,
                 "/api/v1.0/buildable-sets/<string:username>")

api.add_resource(BuildableSetsWithColorFlexibility,
                 "/api/v1.0/buildable-sets-additional/<string:username>")


if __name__ == "__main__":
    app.run(debug=True)  # TODO DO NOT INCLUDE IN PRODUCTION ENVIRONMENT
