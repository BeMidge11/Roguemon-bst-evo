import json, re

with open('RoguemonRevoData.lua', 'r', encoding='utf-8') as f:
    text = f.read()
with open('species_data.json', 'r', encoding='utf-8') as f:
    sdata = {int(k): v for k, v in json.load(f).items()}

abra_match = re.search(r'\[63\]\s*=\s*\{\s*--\s*Abra\s*\n(.*?)\n\s*\},', text, re.DOTALL)
evos = re.findall(r'\{\s*id\s*=\s*(\d+)\s*,\s*perc\s*=\s*([0-9.]+)\s*\}', abra_match.group(1))
for eid, perc in evos[:10]:
    info = sdata[int(eid)]
    print(f"{info['name']}: {perc}% | BST {info['bst']} | Types {info['types']}")
