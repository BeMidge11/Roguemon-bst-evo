import json, re

with open('species_constants.json', 'r', encoding='utf-8') as f:
    species_map = {int(k): v for k, v in json.load(f).items()}

import os
os.environ.pop('SSLKEYLOGFILE', None)
import requests

url = 'https://play.pokemonshowdown.com/data/pokedex.json'
r = requests.get(url, timeout=10)
showdown = r.json()

showdown_by_slug = {}
for k, v in showdown.items():
    showdown_by_slug[k.lower()] = v
    clean_name = re.sub(r'[^a-zA-Z0-9]', '', v.get('name', '')).lower()
    showdown_by_slug[clean_name] = v

with open('RoguemonRevoData.lua', 'r', encoding='utf-8') as f:
    text = f.read()

starter_matches = re.findall(r'\[(\d+)\]\s*=\s*\{\s*--\s*(.+?)\s*\n', text)
print(f"Total starters in Lua: {len(starter_matches)}")

base_form_suffixes = [
    '_NORMAL', '_WEST', '_LAND', '_RED_STRIPED', '_STANDARD', '_SPRING',
    '_INCARNATE', '_ORDINARY', '_ARIA', '_RED', '_NATURAL', '_M', '_SHIELD',
    '_AVERAGE', '_CONFINED', '_BAILE', '_MIDDAY', '_DISGUISED', '_AMPED',
    '_PHONY', '_STRAWBERRY_VANILLA_CREAM', '_ICE', '_SINGLE_STRIKE',
    '_PLANT', '_OVERCAST', '_METEOR_RED', '_FULL_BELLY', '_CHEST',
    '_SOLO', '_ORIGINAL_COLOR', '_AMPED_GMAX', '_LOW_KEY_GMAX',
    '_TWO_SEGMENT', '_FAMILY_OF_FOUR', '_ZERO', '_HERO', '_STARTER'
]

starter_bsts = {}
over_450 = []

for sid_str, sname in starter_matches:
    sid = int(sid_str)
    constant = species_map.get(sid, '')
    clean_const = constant
    for sfx in base_form_suffixes:
        if clean_const.endswith(sfx):
            clean_const = clean_const[:-len(sfx)]
            break

    candidates = [
        re.sub(r'[^a-zA-Z0-9]', '', constant).lower(),
        re.sub(r'[^a-zA-Z0-9]', '', clean_const).lower(),
        re.sub(r'[^a-zA-Z0-9]', '', sname).lower(),
    ]
    hit = None
    for c in candidates:
        if c in showdown_by_slug:
            hit = showdown_by_slug[c]
            break
            
    if hit:
        if 'baseStats' not in hit:
            print(f"Starter {sname} hit has no baseStats: {hit}")
            continue
        bst = sum(hit['baseStats'].values())
        starter_bsts[sname] = bst
        if bst > 450:
            over_450.append((sname, bst))
    else:
        print(f"Starter {sname} (ID {sid}, constant {constant}) not found in Showdown!")

print(f"Starters resolved: {len(starter_bsts)} / {len(starter_matches)}")
print(f"Starters with BST > 450: {len(over_450)}")
for s, bst in over_450[:15]:
    print(f"  {s}: {bst}")
