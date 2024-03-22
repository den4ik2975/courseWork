import json
from database.crud import add_new_variant

with open('resources/test.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

    add_new_variant(data['data'], data['start'], data['end'], data['answers'])