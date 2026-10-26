import os
import json, re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

# 1. Load species constants
constants_file = os.path.join(SCRIPT_DIR, 'species_constants.json')
with open(constants_file, 'r', encoding='utf-8') as f:
    species_map = {int(k): v for k, v in json.load(f).items()}

# 2. Load Showdown pokedex
os.environ.pop('SSLKEYLOGFILE', None)
import requests

url = 'https://play.pokemonshowdown.com/data/pokedex.json'
r = requests.get(url, timeout=10)
showdown = r.json()

# Index showdown entries
showdown_by_slug = {}
for k, v in showdown.items():
    showdown_by_slug[k.lower()] = v
    clean = re.sub(r'[^a-zA-Z0-9]', '', v.get('name', '')).lower()
    showdown_by_slug[clean] = v

# 3. Load Lua file to get all IDs and starter names
lua_file = os.path.join(PROJECT_DIR, 'RoguemonRevoData.lua')
with open(lua_file, 'r', encoding='utf-8') as f:
    text = f.read()

starter_comment_map = {}
for m in re.finditer(r'\[(\d+)\]\s*=\s*\{\s*--\s*(.+?)\s*\n', text):
    starter_comment_map[int(m.group(1))] = m.group(2).strip()

evo_ids = set(int(m) for m in re.findall(r'id\s*=\s*(\d+)', text))
starter_ids = set(int(m) for m in re.findall(r'\[(\d+)\]\s*=', text))
all_ids = sorted(evo_ids.union(starter_ids))

base_form_suffixes = [
    '_NORMAL', '_WEST', '_LAND', '_RED_STRIPED', '_STANDARD', '_SPRING',
    '_INCARNATE', '_ORDINARY', '_ARIA', '_RED', '_NATURAL', '_M', '_SHIELD',
    '_AVERAGE', '_CONFINED', '_BAILE', '_MIDDAY', '_DISGUISED', '_AMPED',
    '_PHONY', '_STRAWBERRY_VANILLA_CREAM', '_ICE', '_SINGLE_STRIKE',
    '_PLANT', '_OVERCAST', '_METEOR_RED', '_FULL_BELLY', '_CHEST',
    '_SOLO', '_ORIGINAL_COLOR', '_AMPED_GMAX', '_LOW_KEY_GMAX',
    '_TWO_SEGMENT', '_FAMILY_OF_FOUR', '_ZERO', '_HERO', '_STARTER'
]

# Special manual overrides for anything unique in Pokeemerald / Roguemon
MANUAL_OVERLAY = {
    1165: {'name': 'Zygarde-10%', 'slug': 'zygarde10', 'types': ['Dragon', 'Ground'], 'bst': 486},
    1166: {'name': 'Zygarde-50%', 'slug': 'zygarde', 'types': ['Dragon', 'Ground'], 'bst': 600},
    1172: {'name': 'Rockruff-Own-Tempo', 'slug': 'rockruff', 'types': ['Rock'], 'bst': 280},
    1309: {'name': 'Maushold', 'slug': 'maushold', 'types': ['Normal'], 'bst': 470},
    1367: {'name': 'Tatsugiri', 'slug': 'tatsugiri', 'types': ['Dragon', 'Water'], 'bst': 475},
    1411: {'name': 'Sinistcha', 'slug': 'sinistcha', 'types': ['Grass', 'Ghost'], 'bst': 508},
    1416: {'name': 'Ogerpon', 'slug': 'ogerpon', 'types': ['Grass'], 'bst': 550},
    # Partner / Starter forms
    1487: {'name': 'Pikachu-Starter', 'slug': 'pikachustarter', 'types': ['Electric'], 'bst': 430},
    1488: {'name': 'Eevee-Starter', 'slug': 'eeveestarter', 'types': ['Normal'], 'bst': 430},
}

resolved_species = {}
unresolved = []

for sid in all_ids:
    if sid in MANUAL_OVERLAY:
        entry = MANUAL_OVERLAY[sid]
        resolved_species[sid] = {
            'name': starter_comment_map.get(sid, entry['name']),
            'slug': entry['slug'],
            'types': entry['types'],
            'bst': entry['bst'],
            'evolution_level': max(1, entry['bst'] // 10)
        }
        continue

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
        if 'baseStats' not in hit and 'baseSpecies' in hit:
            base_hit = showdown_by_slug.get(hit['baseSpecies'].lower())
            if base_hit and 'baseStats' in base_hit:
                hit = base_hit

    if hit and 'baseStats' in hit:
        bst = sum(hit['baseStats'].values())
        types = hit.get('types', ['Normal'])
        name = starter_comment_map.get(sid) or hit.get('name') or constant.replace('_', ' ').title()
        # Clean unicode apostrophe if any
        name = name.replace('’', "'")
        slug = re.sub(r'[^a-zA-Z0-9]', '', hit.get('name', '')).lower()
        resolved_species[sid] = {
            'name': name,
            'slug': slug,
            'types': types,
            'bst': bst,
            'evolution_level': max(1, bst // 10)
        }
    else:
        unresolved.append((sid, lua_name, constant))

print(f"Total Lua IDs: {len(all_ids)}")
print(f"Resolved: {len(resolved_species)} / {len(all_ids)}")
print(f"Unresolved: {len(unresolved)}")
for u in unresolved:
    print("  ", u)

out_file = os.path.join(PROJECT_DIR, 'species_data.json')
with open(out_file, 'w', encoding='utf-8') as f:
    json.dump({str(k): v for k, v in resolved_species.items()}, f, indent=2)

print(f"Saved {out_file} successfully!")
