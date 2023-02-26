from typing import Dict
from collections import namedtuple
import logging
from helpers.api_functions import get_lego_set_details
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, parent_dir)


LegoBrick = namedtuple('LegoBrick', ['id', 'color', 'quantity'])
logging.basicConfig(level=logging.DEBUG)


def find_sets_with_less_bricks_than_users_inventory(lego_sets: Dict[str, any], brick_count: int) -> Dict[str, str]:
    """
    Finds LEGO sets from a given dictionary of sets with total brick count less than or equal to a given brick count.

    Args:
    - lego_sets (Dict[str, any]): A dictionary containing information about LEGO sets, where the 'Sets' key holds a list of sets.
    - brick_count (int): An integer representing the total number of bricks the user has.

    Returns:
    - matching_sets (Dict[str, str]): A dictionary containing information about the matching LEGO sets, where the key is the
    set ID and the value is the set name.
    """
    matching_sets: Dict[str, str] = {}

    for lego_set in lego_sets['Sets']:
        if lego_set['totalPieces'] <= brick_count:
            matching_sets[lego_set['id']] = lego_set['name']

    return matching_sets


def find_buildable_sets(users_inventory: Dict, lego_sets: Dict, is_flexible_on_color: bool = False) -> Dict[str, Dict[str, str]]:
    """
    Finds the buildable sets from Lego sets using the user's inventory.

    Args:
        users_inventory (Dict): A dictionary containing the user's Lego pieces and their quantities.
        lego_sets (Dict): A dictionary containing Lego set details.
        is_flexible_on_color (bool, optional): A flag indicating whether to be flexible on colors. Defaults to False.

    Returns:
        Dict[str, Dict[str, str]]: A dictionary containing the buildable sets that the user can build, with the set name
        as key and the set id as value.
    """
    buildable_sets: Dict[str, Dict[str, str]] = {}
    for lego_set in lego_sets['Sets']:
        lego_set_details = get_lego_set_details(lego_set['id'])
        if lego_set_details is None:
            continue
        if is_flexible_on_color:
            if user_can_build_set_if_colors_are_changeable(users_inventory, lego_set_details['pieces']):
                buildable_sets[lego_set['name']] = {'id': lego_set['id']}
        else:
            if user_can_build_set(users_inventory, lego_set_details['pieces']):
                buildable_sets[lego_set['name']] = {'id': lego_set['id']}

    return buildable_sets


def sort_user_inventory(users_inventory_raw: Dict) -> Dict[str, Dict[str, int]]:
    """
    Given a dictionary `users_inventory_raw` representing a user's Lego collection, returns a sorted version of it
    that maps each piece ID to a dictionary of color variants and their respective counts.

    Args:
        users_inventory_raw (Dict): A dictionary representing a user's Lego collection, with the following format:
            {'collection': [{'pieceId': str,
                             'variants': [{'color': str, 'count': int}, ...]}, ...]}

    Returns:
        Dict: A sorted version of the input `users_inventory_raw` dictionary that maps each piece ID (str) to a
        dictionary of color variants (str) and their respective counts (int), with the following format:
        {piece_id: {color: count, ...}, ...}
    """
    sorted_inventory: Dict[str, Dict[str, int]] = {}

    for piece in users_inventory_raw['collection']:
        piece_id = piece['pieceId']
        sorted_inventory[piece_id] = {}
        for variant in piece['variants']:
            color = str(variant['color'])
            count = variant['count']
            sorted_inventory[piece_id][color] = count

    return sorted_inventory


def user_can_build_set(user_inventory: Dict[str, Dict[str, int]], lego_bricks: Dict) -> bool:
    """
    Check if a user has the right pieces in their inventory to build a given LEGO set.

    Args:
        user_inventory (Dict[str, Dict[str, int]]): A dictionary representing the user's LEGO inventory, where the keys are
            piece IDs and the values are dictionaries representing the colors and quantities of each piece the user has.
        lego_bricks (Dict): A dictionary representing the LEGO bricks needed to build the set, where each element contains
            a part design ID, material, and quantity.

    Returns:
        bool: True if the user has enough pieces to build the set, False otherwise.
    """
    if not user_inventory:
        return False

    for lego in lego_bricks:

        lego_brick = LegoBrick(lego['part']['designID'], str(
            lego['part']['material']), lego['quantity'])

        if lego_brick.id not in user_inventory or lego_brick.color not in user_inventory[lego_brick.id]:
            return False

        if user_inventory[lego_brick.id][lego_brick.color] < lego_brick.quantity:
            return False

    return True


def user_can_build_set_if_colors_are_changeable(user_inventory, lego_bricks_in_set):
    """
    Checks if a given user's inventory contains enough bricks to build a given LEGO if a color substitution is okay with the user. 
    It will not find Lego sets buildable by the user without any substitutions in color.

    Args:
        user_inventory (Dict[str, Dict[str, int]]): A dictionary representing the user's LEGO inventory.
        lego_bricks_in_set (List[Dict[str, any]]): A list of dictionaries representing the LEGO bricks required to build the set.

    Returns:
        bool: True if the user can build the set using their inventory or after making some possible substitutions for missing bricks, False otherwise.
    """
    used_colors = set()
    substitutions = {}
    needs_substitution = False

    if not user_inventory:
        return False

    if user_can_build_set(user_inventory, lego_bricks_in_set):
        return False

    for lego in lego_bricks_in_set:
        lego_brick = LegoBrick(lego['part']['designID'], str(
            lego['part']['material']), lego['quantity'])

        if lego_brick.id in user_inventory:
            # check if the required color is available
            if lego_brick.color in user_inventory[lego_brick.id]:
                # register the color as having been used.
                used_colors.add(lego_brick.color)
            else:
                # try to find a substitute color
                found_substitute = False
                for color, count in user_inventory[lego_brick.id].items():
                    if color not in used_colors and count >= lego_brick.quantity:
                        # use the substitute color
                        used_colors.add(color)
                        substitutions[lego_brick.color] = color
                        found_substitute = True
                        break
                if not found_substitute:
                    needs_substitution = True
                    break
        else:
            # the required brick is not available
            needs_substitution = True
            break

    if not needs_substitution:
        return True

    # Check if substitution is possible
    for lego in lego_bricks_in_set:
        lego_brick = LegoBrick(lego['part']['designID'], str(
            lego['part']['material']), lego['quantity'])
        if lego_brick.color not in substitutions:
            needs_substitution = False
            for color, count in user_inventory[lego_brick.id].items():
                if color not in used_colors and count >= lego_brick.quantity:
                    # register the color as having been used.
                    used_colors.add(color)
                    substitutions[lego_brick.color] = color
                    needs_substitution = True
                    break
            if not needs_substitution:
                # no substitute color found
                return False

    # helping function if we want to see the bricks being substituted.
    # print_substitutions(lego_bricks_in_set, substitutions)
    return True


def print_substitutions(lego_bricks: Dict, substitutions: Dict):
    """
    Prints a list of substitutions made for each building block in the set.

    Args:
    - lego_bricks: A dictionary containing the Lego bricks of the Lego set, with each item
                       specifying the design ID, color, and quantity of a Lego brick required to build
                       the set.
    - substitutions: A dictionary containing the color substitutions made for each Lego brick in the set,
                     where the keys are the original colors and the values are the substitute colors.

    Returns:
    - None
    """
    for building_block in lego_bricks:
        lego_brick = LegoBrick(building_block['part']['designID'], str(
            building_block['part']['material']), building_block['quantity'])
        if lego_brick.color in substitutions:
            print(
                f"{lego_brick.quantity} x {lego_brick.color} (substituted with {substitutions[lego_brick.color]})")
