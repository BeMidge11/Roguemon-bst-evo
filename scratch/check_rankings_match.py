import json

with open('starter_rankings.json', 'r', encoding='utf-8') as f:
    rankings = json.load(f)

ranking_names = [r['name'] for r in rankings]

with open('RoguemonRevoData.lua', 'r', encoding='utf-8') as f:
    text = f.read()

import re
lua_starters = [m[1].strip() for m in re.findall(r'\[(\d+)\]\s*=\s*\{\s*--\s*(.+?)\s*\n', text)]

print(f"Starters in rankings: {len(ranking_names)}")
print(f"Starters in Lua: {len(lua_starters)}")

missing_from_lua = []
for r in ranking_names:
    if r in lua_starters:
        continue
    # Check if a normalized version exists:
    # e.g., 'Growlithe H' -> 'Growlithe-H'
    alt = r.replace(' H', '-H').replace(' G', '-G').replace(' A', '-A').replace(' P', '-P')
    if alt in lua_starters:
        continue
    missing_from_lua.append(r)

print(f"Rankings starters missing from Lua: {len(missing_from_lua)}")
for m in missing_from_lua[:20]:
    print("  ", m)
