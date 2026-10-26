import json, re

with open('species_constants.json', 'r', encoding='utf-8') as f:
    species_map = {int(k): v for k, v in json.load(f).items()}

with open('pokemon_data_cache.json', 'r', encoding='utf-8') as f:
    cache = json.load(f)

with open('RoguemonRevoData.lua', 'r', encoding='utf-8') as f:
    text = f.read()

evo_ids = set(int(m) for m in re.findall(r'id\s*=\s*(\d+)', text))
starter_ids = set(int(m) for m in re.findall(r'\[(\d+)\]\s*=', text))
all_ids = sorted(evo_ids.union(starter_ids))

print(f"Total unique species IDs in Lua: {len(all_ids)}")

# Let's see how each ID maps to cache
# Cache keys are capitalized names, e.g. 'Abra', 'Duosion', 'Pikachup', etc.
cache_lower = {k.lower(): v for k, v in cache.items()}

# We also have starter comments in Lua
starter_comment_map = {}
for m in re.finditer(r'\[(\d+)\]\s*=\s*\{\s*--\s*(.+?)\s*\n', text):
    starter_comment_map[int(m.group(1))] = m.group(2).strip()

matched_in_cache = 0
unmatched = []

for sid in all_ids:
    constant = species_map.get(sid, '')
    lua_name = starter_comment_map.get(sid, '')
    
    # Try different ways to find in cache:
    found = False
    candidates = [
        lua_name,
        lua_name.lower(),
        constant,
        constant.lower(),
        constant.replace('_', '-').lower(),
        constant.replace('_', '').lower(),
        constant.title().replace('_', '')
    ]
    for c in candidates:
        if c in cache:
            found = True
            break
        if c.lower() in cache_lower:
            found = True
            break
    if found:
        matched_in_cache += 1
    else:
        unmatched.append((sid, lua_name, constant))

print(f"Matched in cache: {matched_in_cache} / {len(all_ids)}")
print(f"Unmatched: {len(unmatched)}")
print("Sample unmatched (first 25):")
for u in unmatched[:25]:
    print(u)
