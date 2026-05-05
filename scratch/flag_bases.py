import json

JSON_FILE = "random_bst_evolutions.json"

with open(JSON_FILE, "r", encoding="utf-8") as f:
    json_data = json.load(f)

# 1. Identify all Pokémon that are TARGETS of an evolution
all_evolutions = set()
for name in json_data:
    for evo in json_data[name].get("evolutions", []):
        all_evolutions.add(evo["evolution"])

# 2. Flag 'Base Forms' (those that are NOT the result of an evolution)
for name in json_data:
    # If a Pokémon is NOT an evolution of something else, it's a base form.
    # Note: This effectively identifies the 95ish "starters" of your perfect list.
    json_data[name]["is_base"] = (name not in all_evolutions)

with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(json_data, f, indent=2)

print("Flagged base forms in the evolution data.")
