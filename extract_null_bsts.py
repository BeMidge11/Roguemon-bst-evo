import json
from collections import defaultdict

INPUT = "random_bst_evolutions.json"
OUTPUT = "bst_missing.json"

with open(INPUT, "r", encoding="utf-8") as f:
    data = json.load(f)

missing = defaultdict(set)

for starter, entry in data.items():
    for evo in entry["evolutions"]:
        if evo["bst"] is None:
            missing[evo["evolution"]].add(starter)

out = {
    name: {
        "bst": None,
        "appears_in": sorted(list(starters))
    }
    for name, starters in sorted(missing.items())
}

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2)

print(f"Found {len(out)} Pokémon with missing BSTs")
print(f"Wrote {OUTPUT}")
