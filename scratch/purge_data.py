import json

JSON_FILE = "random_bst_evolutions.json"

with open(JSON_FILE, "r", encoding="utf-8") as f:
    json_data = json.load(f)

# The "Perfect" Rule: 
# 1. BST <= 450
# 2. No vanilla evolution (forced: false)
# 3. Not on the explicit 'polluter' list (Frillish, Sneasel, etc.)

blacklist = ["frillish", "sneasel", "pumpkaboo"]

cleaned_data = {}
for name, entry in json_data.items():
    is_blacklisted = any(b in name.lower() for b in blacklist)
    
    if entry.get("base_bst", 0) <= 450 and not entry.get("forced", False) and not is_blacklisted:
        cleaned_data[name] = entry

# Preserve the Porygon family and other specific cases if they were forced but allowed?
# No, the user said "does not evo" (meaning no vanilla evolution).
# So we keep ONLY the non-forced ones under 451.

with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(cleaned_data, f, indent=2)

print(f"Cleaned JSON: Reduced from {len(json_data)} to {len(cleaned_data)} perfect entries.")
