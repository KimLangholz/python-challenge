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
from routes import routes_bp

app = Flask(__name__)
api = Api(app)


app.register_blueprint(routes_bp)


class BuildableSetsFromCurrentInventory(Resource):
    """
    Resource class for finding buildable sets from a user's current inventory.
    """

    logging.basicConfig(level=logging.DEBUG)
    cache = TTLCache(maxsize=1000, ttl=180)

    def get(self, username: str) -> Dict[str, Any]:
        """
        Returns a list of buildable sets from a user's current inventory.

        Args:
            username (str): The username of the user whose inventory will look through to find buildable sets.

        Returns:
            A dictionary containing a list of buildable sets from current inventory
        """
        try:
            user_data = get_user_data(username)

            lego_sets: Dict[str, Any] = get_lego_sets()

            sets_buildable_with_users_lego_count: Dict[str, str] = find_sets_with_less_bricks_than_users_inventory(
                lego_sets, user_data['brickCount'])

            if not sets_buildable_with_users_lego_count:
                return {"message": "No buildable sets found."}

            users_inventory: Dict[str, Any] = sort_user_inventory(
                get_user_inventory_details(user_data))

            buildable_sets: Dict[str, Dict[str, str]] = find_buildable_sets(
                users_inventory, lego_sets, False)

            return {"buildable_sets": buildable_sets}

        except requests.exceptions.HTTPError as err:
            logging.error(f"Request error: {err}")
            return {"message": "An error occurred while retrieving user data."}

        except Exception as err:
            logging.error(f"An error occurred: {err}")
            return {"message": "An error occurred."}


class BuildableSetsWithColorFlexibility(Resource):
    """
    Resource class for finding sets that can be build from a user's current inventory if they're swapping out at least one color.
    """
    logging.basicConfig(level=logging.DEBUG)
    cache = TTLCache(maxsize=1000, ttl=180)

    def get(self, username: str) -> Dict[str, Any]:
        """
        Returns a list of sets a user could build if they're willing to swap at least one color out with another 
        unused color in the inventory for an entire compoent. e.g. a red roof becomes a pink roof.

        Args:
            username (str): The username of the user whose inventory will look through to find buildable sets.

        Returns:
            A dictionary containing a list of sets a user can build if they're swapping colors out.
        """
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

            buildable_sets: Dict[str, Dict[str, str]] = find_buildable_sets(
                users_inventory, lego_sets, True)

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
