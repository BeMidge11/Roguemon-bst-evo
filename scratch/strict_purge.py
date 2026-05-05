import json
import os

JSON_FILE = "random_bst_evolutions.json"
CACHE_FILE = "vanilla_evos_cache.json"

with open(JSON_FILE, "r", encoding="utf-8") as f:
    json_data = json.load(f)
with open(CACHE_FILE, "r", encoding="utf-8") as f:
    vanilla_evos_list = json.load(f)

# The cache is a list of lowercase names that HAVE an evolution
natural_evolvers = set(name.lower() for name in vanilla_evos_list)

print(f"Current entries: {len(json_data)}")

cleaned_data = {}
for name, entry in json_data.items():
    # THE RULES:
    # 1. BST must be 450 or under.
    # 2. It must NOT have a natural vanilla evolution.
    # 3. It must NOT be on our manual polluter blacklist.
    
    is_low_bst = entry.get("base_bst", 0) <= 450
    # Check lowercase name against the natural evolvers list
    is_not_natural_evolver = (name.lower() not in natural_evolvers)
    
    # Handle regional forms (the cache usually has base names)
    if is_not_natural_evolver and name.endswith((" H", " G", " A", " P")):
        base_name = name[:-2].lower()
        if base_name in natural_evolvers:
            is_not_natural_evolver = False

    is_not_blacklisted = not any(b in name.lower() for b in ["frillish", "sneasel", "pumpkaboo"])
    
    if is_low_bst and is_not_natural_evolver and is_not_blacklisted:
        cleaned_data[name] = entry

with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(cleaned_data, f, indent=2)

print(f"Final perfect entries: {len(cleaned_data)}")
print("JSON has been purged of all natural evolvers.")
