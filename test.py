import json
from database.crud import add_new_variant, get_random_variant
from utils.helper_functions import pair_checker

def add():
    with open('resources/test.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

        add_new_variant(data['data'], data['start'], data['end'], data['answers'])


def try_to_get():
    var = get_random_variant()
    ans = pair_checker(var.connections)
    print(ans)

try_to_get()