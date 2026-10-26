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

evo_ids = set(int(m) for m in re.findall(r'id\s*=\s*(\d+)', text))
starter_ids = set(int(m) for m in re.findall(r'\[(\d+)\]\s*=', text))
all_ids = sorted(evo_ids.union(starter_ids))

starter_comment_map = {}
for m in re.finditer(r'\[(\d+)\]\s*=\s*\{\s*--\s*(.+?)\s*\n', text):
    starter_comment_map[int(m.group(1))] = m.group(2).strip()

base_form_suffixes = [
    '_NORMAL', '_WEST', '_LAND', '_RED_STRIPED', '_STANDARD', '_SPRING',
    '_INCARNATE', '_ORDINARY', '_ARIA', '_RED', '_NATURAL', '_M', '_SHIELD',
    '_AVERAGE', '_CONFINED', '_BAILE', '_MIDDAY', '_DISGUISED', '_AMPED',
    '_PHONY', '_STRAWBERRY_VANILLA_CREAM', '_ICE', '_SINGLE_STRIKE',
    '_PLANT', '_OVERCAST', '_METEOR_RED', '_FULL_BELLY', '_CHEST',
    '_SOLO', '_ORIGINAL_COLOR', '_AMPED_GMAX', '_LOW_KEY_GMAX',
    '_TWO_SEGMENT', '_FAMILY_OF_FOUR', '_ZERO', '_HERO'
]

matched = 0
unmatched = []

for sid in all_ids:
    constant = species_map.get(sid, '')
    lua_name = starter_comment_map.get(sid, '')
    
    clean_const = constant
    for sfx in base_form_suffixes:
        if clean_const.endswith(sfx):
            clean_const = clean_const[:-len(sfx)]
            break

    candidates = [
        re.sub(r'[^a-zA-Z0-9]', '', constant).lower(),
        re.sub(r'[^a-zA-Z0-9]', '', clean_const).lower(),
        re.sub(r'[^a-zA-Z0-9]', '', lua_name).lower(),
        constant.lower(),
        clean_const.lower(),
        lua_name.lower()
    ]
    
    hit = None
    for c in candidates:
        if c in showdown_by_slug:
            hit = showdown_by_slug[c]
            break
            
    if hit:
        matched += 1
    else:
        unmatched.append((sid, lua_name, constant))

print(f"Matched directly against Showdown: {matched} / {len(all_ids)}")
print(f"Unmatched: {len(unmatched)}")
for u in unmatched:
    try:
        print(f"{u[0]}: Lua='{u[1]}' Constant='{u[2]}'")
    except:
        pass
