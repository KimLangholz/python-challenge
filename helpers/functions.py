import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, parent_dir)

from helpers.api_functions import get_lego_set_details
import logging
from collections import namedtuple
from typing import Dict

LegoBrick = namedtuple('LegoBrick', ['id', 'color', 'quantity'])
logging.basicConfig(level=logging.DEBUG)

def find_sets_with_less_bricks_than_users_inventory(lego_sets: Dict[str, any], brick_count: int) -> Dict[str, str]:
    matching_sets: Dict[str, str] = {}

    for lego_set in lego_sets['Sets']:
        if lego_set['totalPieces'] <= brick_count:
            matching_sets[lego_set['id']] = lego_set['name']

    return matching_sets

def find_buildable_sets(users_inventory: Dict, lego_sets: Dict, is_flexible_on_color: bool = False) -> Dict[str, Dict[str, str]]:
    # Configuring logging for debugging errors.
    logging.basicConfig(level=logging.ERROR)

    # Find buildable sets from Lego sets
    buildable_sets: Dict[str, Dict[str, str]] = {}
    for lego_set in lego_sets['Sets']:
        lego_set_details = get_lego_set_details(lego_set['id'])
        if lego_set_details is None:
            continue
        if is_flexible_on_color:
            if can_build_set_if_colors_are_changeable(users_inventory, lego_set_details['pieces']):
                buildable_sets[lego_set['name']] = {'id': lego_set['id']}
        else:
            if can_build_set(users_inventory, lego_set_details['pieces']):
                buildable_sets[lego_set['name']] = {'id': lego_set['id']}

    # Return the buildable sets we've found for the user.
    return buildable_sets

def sort_user_inventory(users_inventory_raw: Dict) -> Dict[str, Dict[str, int]]:
    return {piece['pieceId']: {str(variant['color']): variant['count']
                               for variant in piece['variants']} for piece in users_inventory_raw['collection']}


def can_build_set(user_inventory: Dict[str, Dict[str, int]], lego_bricks: Dict) -> bool:

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

def can_build_set_if_colors_are_changeable(user_inventory, lego_bricks_in_set):
    used_colors = set()
    substitutions = {}
    needs_substitution = False

    if not user_inventory:
        return False

    if can_build_set(user_inventory, lego_bricks_in_set):
        return False

    for lego in lego_bricks_in_set:
        lego_brick = LegoBrick(lego['part']['designID'], str(
            lego['part']['material']), lego['quantity'])

        if lego_brick.id in user_inventory:
            # check if the required color is available
            if lego_brick.color in user_inventory[lego_brick.id]:
                # use the required color
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
                    # no substitute color found
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
                    # use the substitute color
                    used_colors.add(color)
                    substitutions[lego_brick.color] = color
                    needs_substitution = True
                    break
            if not needs_substitution:
                # no substitute color found
                return False

    print_substitutions(lego_bricks_in_set, substitutions)
    return True


def print_substitutions(building_blocks: Dict, substitutions: Dict):
    for building_block in building_blocks:
        lego_brick = LegoBrick(building_block['part']['designID'], str(
            building_block['part']['material']), building_block['quantity'])
        if lego_brick.color in substitutions:
            print(f"{lego_brick.quantity} x {lego_brick.color} (substituted with {substitutions[lego_brick.color]})")

