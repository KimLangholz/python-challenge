import os
import sys
import unittest

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, parent_dir)

from helpers.functions import *


class TestSortUserInventory(unittest.TestCase):

    def test_sort_user_inventory_returns_expected_result(self):
        """
        Test that the sort_user_inventory function returns the expected sorted user inventory dictionary.

        The function should take a user inventory dictionary that contains a collection key, which maps to a list of items. Each item in the collection should have a pieceId key that maps to a string value and a variants key that maps to a list of dictionaries. Each dictionary in the variants list should have a color key that maps to a string value and a count key that maps to an integer value. The function should sort the user inventory by pieceId and then by color and return a dictionary where the keys are the pieceIds and the values are dictionaries that map colors to counts.

        Inputs:
        - user_inventory_raw (dict): A dictionary that contains a collection key, which maps to a list of items. Each item should have a pieceId key that maps to a string value and a variants key that maps to a list of dictionaries. Each dictionary in the variants list should have a color key that maps to a string value and a count key that maps to an integer value.

        Output:
        - A dictionary where the keys are the pieceIds and the values are dictionaries that map colors to counts, sorted by pieceId and then by color.
        """
        user_inventory_raw = {
            'collection': [
                {
                    'pieceId': '1234',
                    'variants': [
                        {'color': 'Red', 'count': 5},
                        {'color': 'Blue', 'count': 10}
                    ]
                },
                {
                    'pieceId': '5678',
                    'variants': [
                        {'color': 'Green', 'count': 3},
                        {'color': 'Yellow', 'count': 8}
                    ]
                }
            ]
        }

        expected_result_after_sort = {
            '1234': {'Red': 5, 'Blue': 10},
            '5678': {'Green': 3, 'Yellow': 8}
        }

        sorted_inventory = sort_user_inventory(user_inventory_raw)

        self.assertEqual(sorted_inventory, expected_result_after_sort)

    def test_sort_user_inventory_raises_exception_with_no_data(self):
        """
        Test that the sort_user_inventory function raises a KeyError when given an empty user inventory dictionary.

        The function should take a user inventory dictionary that contains a collection key, which maps to a list of items. 
        If the collection is empty or does not exist, the function should raise a KeyError.

        Inputs:
        - An empty dictionary.

        Output:
        - A KeyError when the user inventory is empty or does not exist.
        """
        with self.assertRaises(KeyError):
            sort_user_inventory({})

    def test_sort_user_inventory_with_empty_collection(self):
        """
        Test that the sort_user_inventory function returns an empty dictionary when given an empty collection.

        The function should take a user inventory dictionary that contains a collection key, which maps to a list of items. 
        If the collection is empty, the function should return an empty dictionary.

        Inputs:
        - user_inventory_raw (dict): A dictionary that contains a collection key, which maps to a list of items.

        Output:
        - An empty dictionary if the collection is empty.
        """

        user_inventory_raw = {
            'collection': [
            ]
        }

        expected_result_after_sort = {}

        self.assertEqual(sort_user_inventory(
            user_inventory_raw), expected_result_after_sort)


class TestCanBuildSet(unittest.TestCase):

    def test_user_can_build_set_returns_true_for_valid_inventory(self):
        """
        Test that the user_can_build_set function returns True when given a user inventory matching the required lego bricks in a set.

        The function should take a user inventory dictionary that maps design IDs to material and quantities, 
        and a list of lego bricks, where each lego brick is a dictionary that specifies a design ID, the required material/color, 
        and the quantity of bricks required. The function should return True if the user inventory has enough materials to build the specified set, and False otherwise.

        Inputs:
        - user_inventory_sorted (dict): A dictionary that maps design IDs to material:quantities.
        - lego_bricks_in_set (list): A list of dictionaries, where each dictionary specifies a design ID, the required material quantity, and the quantity of blocks required.

        Output:
        - True if the user inventory has enough bricks to build the specified set, and False otherwise.
        """

        user_inventory = {
            '1234': {'5': 5, '4': 10},
            '5678': {'3': 3, '2': 8}
        }

        lego_bricks_in_set = [
            {'part': {'designID': '1234', 'material': 5}, 'quantity': 2},
            {'part': {'designID': '5678', 'material': 3}, 'quantity': 1},
        ]

        self.assertTrue(user_can_build_set(
            user_inventory, lego_bricks_in_set))

    def test_user_can_build_set_returns_false_for_insufficient_quantity(self):
        """
        Test that the user_can_build_set function returns False when given a user inventory doesn't have the quantities of a lego brick required in a set.

        The function should take a user inventory dictionary that maps design IDs to material and quantities, 
        and a list of lego bricks, where each lego brick is a dictionary that specifies a design ID, the required material/color, 
        and the quantity of bricks required. The function should return False if the user inventory is short by at least a single brick required to build the set, and True otherwise.

        Inputs:
        - user_inventory_sorted (dict): A dictionary that maps design IDs to material:quantities.
        - lego_bricks_in_set (list): A list of dictionaries, where each dictionary specifies a design ID, the required quantity, and the quantity of blocks required.

        Output:
        - True if the user inventory has enough bricks to build the specified set, and False otherwise.
        """

        user_inventory = {
            '1234': {'5': 5, '4': 10},
            '5678': {'3': 3, '2': 8}
        }

        lego_bricks_in_set = [
            {'part': {'designID': '1234', 'material': 5}, 'quantity': 6},
            {'part': {'designID': '5678', 'material': 3}, 'quantity': 1},
        ]

        self.assertFalse(user_can_build_set(
            user_inventory, lego_bricks_in_set))

    def test_user_can_build_set_returns_false_for_missing_color(self):
        """
        Test that the user_can_build_set function returns False when given a user inventory doesn't have a brick in the needed color required in a set.

        The function should take a user inventory dictionary that maps design IDs to material and quantities, 
        and a list of lego bricks, where each lego brick is a dictionary that specifies a design ID, the required material/color, 
        and the quantity of bricks required. The function should return False if the user inventory is missing at least one brick in a specific color required to build the set, and True otherwise.

        Inputs:
        - user_inventory_sorted (dict): A dictionary that maps design IDs to material:quantities.
        - lego_bricks_in_set (list): A list of dictionaries, where each dictionary specifies a design ID, the required material quantity, and the quantity of blocks required.

        Output:
        - True if the user inventory has enough bricks to build the specified set, and False otherwise.
        """

        user_inventory = {
            '1234': {'5': 5, '6': 10},
            '5678': {'4': 3, '2': 8}
        }

        lego_bricks_in_set = [
            {'part': {'designID': '1234', 'material': 3}, 'quantity': 2},
            {'part': {'designID': '5678', 'material': 4}, 'quantity': 1},
        ]

        self.assertFalse(user_can_build_set(
            user_inventory, lego_bricks_in_set))


def test_user_can_build_set_if_colors_are_changeable():
    """
    This function tests the behavior of user_can_build_set_if_colors_are_changeable() with different inputs. It tests cases 
    where the function should return False (i.e., the user has enough LEGO bricks of the required design ID and color so no 
    substitution is required), cases where the function should return False (i.e., the user does not have enough LEGO bricks 
    of the required design ID or the required color), and cases where the function should return True because the user has 
    enough LEGO bricks of the required design ID but not of the required color, and color substitutions are allowed and possible.

    Args:
        user_inventory (Dict[str, Dict[str, int]]): A dictionary representing the user's inventory of LEGO bricks.
        lego_bricks_in_set (List[Dict]): A list of dictionaries representing the LEGO bricks required to build a set.

    Returns:
        None.

    Raises:
        AssertionError: If the function returns unexpected output for any of the tested inputs.
    """

    user_inventory = {
        "3001": {"5": 10, "3": 5},
        "3003": {"2": 20},
        "3004": {"5": 5, "4": 10},
        "3005": {"0": 5, "1": 15},
    }

    lego_bricks_in_set = [
        {"part": {"designID": "3001", "material": "5"}, "quantity": 6},
        {"part": {"designID": "3003", "material": "2"}, "quantity": 4},
        {"part": {"designID": "3004", "material": "4"}, "quantity": 2},
        {"part": {"designID": "3005", "material": "1"}, "quantity": 4},
    ]

    assert user_can_build_set(user_inventory, lego_bricks_in_set) == True
    assert user_can_build_set_if_colors_are_changeable(
        user_inventory, lego_bricks_in_set) == False

    lego_bricks_in_set = [
        {"part": {"designID": "3001", "material": "3"}, "quantity": 6},
        {"part": {"designID": "3003", "material": "2"}, "quantity": 4},
        {"part": {"designID": "3004", "material": "4"}, "quantity": 2},
        {"part": {"designID": "3005", "material": "1"}, "quantity": 4},
    ]

    assert user_can_build_set(user_inventory, lego_bricks_in_set) == False
    assert user_can_build_set_if_colors_are_changeable(
        user_inventory, lego_bricks_in_set) == True

    lego_bricks_in_set = [
        {"part": {"designID": "3001", "material": "3"}, "quantity": 6},
        {"part": {"designID": "3003", "material": "2"}, "quantity": 4},
        {"part": {"designID": "3004", "material": "4"}, "quantity": 2},
        {"part": {"designID": "3005", "material": "0"}, "quantity": 12},
    ]

    assert user_can_build_set(user_inventory, lego_bricks_in_set) == False
    assert user_can_build_set_if_colors_are_changeable(
        user_inventory, lego_bricks_in_set) == True

    user_inventory = {}
    lego_bricks_in_set = [
        {"part": {"designID": "3001", "material": "5"}, "quantity": 6},
        {"part": {"designID": "3003", "material": "2"}, "quantity": 4},
        {"part": {"designID": "3004", "material": "4"}, "quantity": 2},
        {"part": {"designID": "3005", "material": "1"}, "quantity": 4},
    ]

    assert user_can_build_set(user_inventory, lego_bricks_in_set) == False
    assert user_can_build_set_if_colors_are_changeable(
        user_inventory, lego_bricks_in_set) == False


if __name__ == '__main__':
    unittest.main()
