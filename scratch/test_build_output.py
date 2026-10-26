import json, re

with open('species_data.json', 'r', encoding='utf-8') as f:
    species_data = {int(k): v for k, v in json.load(f).items()}

with open('RoguemonRevoData.lua', 'r', encoding='utf-8') as f:
    text = f.read()

starter_blocks = re.findall(r'\s*\[(\d+)\]\s*=\s*\{\s*--\s*(.+?)\s*\n(.*?)\n\s*\},', text, re.DOTALL)
print(f"Total starter blocks in Lua: {len(starter_blocks)}")

result = {}
TOTAL_RUNS = 12000

for sid_str, sname_hint, block in starter_blocks:
    sid = int(sid_str)
    s_info = species_data.get(sid)
    if not s_info:
        print(f"Warning: Starter ID {sid} not in species_data")
        continue

    # Use the starter name from the Lua comment, cleaned
    sname = sname_hint.strip()
    base_bst = s_info['bst']

    evo_matches = re.findall(r'\{\s*id\s*=\s*(\d+)\s*,\s*perc\s*=\s*([0-9.]+)\s*\}', block)
    processed = []
    
    for eid_str, perc_str in evo_matches:
        eid = int(eid_str)
        perc = float(perc_str)
        e_info = species_data.get(eid)
        if not e_info:
            print(f"Warning: Evo ID {eid} not in species_data")
            continue

        processed.append({
            "evolution": e_info['name'],
            "bst": e_info['bst'],
            "types": e_info['types'],
            "evolution_level": e_info['evolution_level'],
            "probability": round(perc / 100.0, 6)
        })

    if not processed:
        continue

    processed.sort(key=lambda x: (x["bst"] is None, x["bst"] if x["bst"] is not None else 0))
    result[sname] = {
        "base_bst": base_bst,
        "rule": "bst/10",
        "forced": False,
        "types": s_info['types'],
        "evolutions": processed
    }

print(f"Successfully generated {len(result)} starters in result!")
print(f"Sample starter 'Abra':")
print(f"  Base BST: {result['Abra']['base_bst']}")
print(f"  Types: {result['Abra']['types']}")
print(f"  Evolutions count: {len(result['Abra']['evolutions'])}")
print(f"  First 3 evolutions: {result['Abra']['evolutions'][:3]}")
print(f"Sample starter 'Pikachu': {result.get('Pikachu', {}).get('base_bst')}")
print(f"Sample starter 'Bulbasaur': {result.get('Bulbasaur', {}).get('base_bst')}")
print(f"Sample starter 'Ponyta-G': {result.get('Ponyta-G', {}).get('base_bst')}")
print(f"Sample starter 'Basculin-W': {result.get('Basculin-W', {}).get('base_bst')}")
