import json
import re

# Known typos and types
TYPE_MAP = {
    'poion': 'Poison', 'posion': 'Poison', 'stteel': 'Steel', 'fighing': 'Fighting', 'psyhcic': 'Psychic',
    'grass': 'Grass', 'ice': 'Ice', 'dark': 'Dark', 'fairy': 'Fairy', 'dragon': 'Dragon', 'ghost': 'Ghost',
    'water': 'Water', 'poison': 'Poison', 'bug': 'Bug', 'fire': 'Fire', 'ground': 'Ground', 'steel': 'Steel',
    'flying': 'Flying', 'normal': 'Normal', 'fighting': 'Fighting', 'electric': 'Electric', 'psychic': 'Psychic', 'rock': 'Rock'
}

manual_data = {}
with open('unknownmons', 'r', encoding='utf-8') as f:
    for line in f:
        # Normalize special characters like curly quotes
        line = line.replace('’', "'").replace('‘', "'")
        
        # Find the name (first word or before comma/space)
        # We handle 'Farfetch'd' specifically as it contains a quote
        match = re.match(r'^\s*([^,:\s]+)', line)
        if match:
            name = match.group(1).strip()
            # If the name is 'Farfetch' or 'Sirfetch', it might have truncated at the quote
            if name.lower() in ['farfetch', 'sirfetch']:
                name = name + "'d"
            
            # Find all words that look like types
            found_types = []
            words = re.split(r'[,\s]+', line)
            for word in words:
                w = word.lower().strip()
                if w in TYPE_MAP:
                    found_types.append(TYPE_MAP[w])
            
            if name and found_types:
                manual_data[name] = found_types

print(f"Loaded {len(manual_data)} manual type mappings.")

with open('random_bst_evolutions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

count = 0
unique_names_patched = set()

for starter in data.values():
    for evo in starter['evolutions']:
        name = evo['evolution']
        
        # Try direct match
        target = name
        # Also try normalizing the name in the JSON to match our manual file
        norm_name = name.replace('’', "'").replace('‘', "'")
        
        if target in manual_data:
            evo['types'] = manual_data[target]
            unique_names_patched.add(name)
            count += 1
        elif norm_name in manual_data:
            evo['types'] = manual_data[norm_name]
            unique_names_patched.add(name)
            count += 1

with open('random_bst_evolutions.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f'Done! Patched {count} total entries ({len(unique_names_patched)} unique Pokémon).')
