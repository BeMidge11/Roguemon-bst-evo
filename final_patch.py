import json
import requests
import os
import time

def normalize(name):
    # Strip common non-alphanumeric chars
    n = name.lower().strip().replace(' ', '-').replace('.', '').replace("'", "").replace(':', '')
    
    specials = {
        'type-null': 'type-null', 
        'farfetchd': 'farfetchd', 
        'sirfetchd': 'sirfetchd', 
        'mr-mimeg': 'mr-mime-galar', 
        'muka': 'muk-alola'
    }
    if n in specials:
        return specials[n]
        
    suffix_map = {
        'm': '-mega', 
        'h': '-hisui', 
        'g': '-galar', 
        'a': '-alola', 
        'p': '-paldea', 
        'f': '-female', 
        'w': '-water', 
        's': '-sandy', 
        't': '-trash', 
        'c': '-core', 
        'l': '-large', 
        'x': '-super',
        'e': '-eternal'
    }
    
    if len(n) > 3 and n[-1] in suffix_map:
        return n[:-1] + suffix_map[n[-1]]
    return n

print("Loading data...")
with open('random_bst_evolutions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

if os.path.exists('pokemon_data_cache.json'):
    with open('pokemon_data_cache.json', 'r', encoding='utf-8') as f:
        cache = json.load(f)
else:
    cache = {}

unknowns = set(e['evolution'] for s in data.values() for e in s['evolutions'] if 'Unknown' in e.get('types', []))
print(f'Fetching {len(unknowns)} missing types...')

for i, name in enumerate(unknowns, 1):
    if name in cache and 'types' in cache[name]:
        continue
    
    slug = normalize(name)
    try:
        r = requests.get(f'https://pokeapi.co/api/v2/pokemon/{slug}', timeout=5)
        if r.status_code == 200:
            cache[name] = {'types': [t['type']['name'].capitalize() for t in r.json()['types']]}
        else:
            # Fallback to base name if suffix failed
            base = slug.split('-')[0]
            r = requests.get(f'https://pokeapi.co/api/v2/pokemon/{base}', timeout=5)
            if r.status_code == 200:
                cache[name] = {'types': [t['type']['name'].capitalize() for t in r.json()['types']]}
            else:
                cache[name] = {'types': ['Unknown']}
    except:
        pass
    
    if i % 20 == 0:
        print(f"Processed {i}/{len(unknowns)}...")
    time.sleep(0.02)

print("Patching JSON...")
for s in data.values():
    for e in s['evolutions']:
        if e['evolution'] in cache:
            e['types'] = cache[e['evolution']]['types']

with open('random_bst_evolutions.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

with open('pokemon_data_cache.json', 'w', encoding='utf-8') as f:
    json.dump(cache, f, indent=2)

print('Done!')
