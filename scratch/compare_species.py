import json, re

with open('species_constants.json', 'r', encoding='utf-8') as f:
    species_map = {int(k): v for k, v in json.load(f).items()}

with open('RoguemonRevoData.lua', 'r', encoding='utf-8') as f:
    text = f.read()

starter_matches = re.findall(r'\[(\d+)\]\s*=\s*\{\s*--\s*(.+?)\s*\n', text)
print('Comparing first 30 starters in Lua with species_constants:')
for sid_str, sname in starter_matches[:30]:
    sid = int(sid_str)
    cname = species_map.get(sid)
    print(f"{sid}: Lua='{sname}' | Constant='{cname}'")
