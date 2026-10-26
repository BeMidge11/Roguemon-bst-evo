import json, re

with open('species_constants.json', 'r', encoding='utf-8') as f:
    species_map = {int(k): v for k, v in json.load(f).items()}

import os
os.environ.pop('SSLKEYLOGFILE', None)
import requests

url = 'https://play.pokemonshowdown.com/data/pokedex.json'
r = requests.get(url, timeout=10)
showdown = r.json()

# Let's index showdown by id (num + forme), name, clean slug
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

matched = 0
unmatched = []

for sid in all_ids:
    constant = species_map.get(sid, '')
    lua_name = starter_comment_map.get(sid, '')
    
    # Generate slug candidates:
    candidates = [
        re.sub(r'[^a-zA-Z0-9]', '', constant).lower(),
        re.sub(r'[^a-zA-Z0-9]', '', lua_name).lower(),
        constant.lower(),
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
for u in unmatched[:30]:
    try:
        print(f"{u[0]}: Lua='{u[1]}' Constant='{u[2]}'")
    except:
        pass
