import json, re

with open('species_constants.json', 'r', encoding='utf-8') as f:
    species_map = {int(k): v for k, v in json.load(f).items()}

with open('RoguemonRevoData.lua', 'r', encoding='utf-8') as f:
    text = f.read()

starter_matches = re.findall(r'\[(\d+)\]\s*=\s*\{\s*--\s*(.+?)\s*\n', text)
forms = []
for sid_str, sname in starter_matches:
    sid = int(sid_str)
    cname = species_map.get(sid, '')
    if '-' in sname or '_' in cname:
        forms.append((sid, sname, cname))

print(f"Total form starters: {len(forms)}")
for sid, sname, cname in forms[:40]:
    print(f"{sid}: Lua='{sname}' <-> Constant='{cname}'")
