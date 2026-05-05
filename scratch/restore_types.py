import json
import os

JSON_FILE = "random_bst_evolutions.json"
CACHE_FILE = "pokemon_data_cache.json"

with open(JSON_FILE, "r", encoding="utf-8") as f:
    json_data = json.load(f)
with open(CACHE_FILE, "r", encoding="utf-8") as f:
    cache_data = json.load(f)

def get_best_data(name, cache):
    # Try exact match first
    if name in cache: return cache[name]
    
    # Try regional variants
    if name.endswith(" H"):
        hisui_name = name.replace(" H", "-Hisui") # Example: Growlithe-Hisui
        if hisui_name in cache: return cache[hisui_name]
    
    # Try case-insensitive
    for k in cache:
        if name.lower() == k.lower():
            return cache[k]
            
    return None

updated_count = 0
for name in json_data:
    entry = json_data[name]
    
    # Top-level types
    current_types = entry.get("types", ["Unknown"])
    if "Unknown" in current_types:
        data = get_best_data(name, cache_data)
        if data:
            entry["types"] = data.get("types", ["Unknown"])
            entry["base_bst"] = data.get("bst", entry.get("base_bst", 400))
            updated_count += 1
            
    # Evolutions
    for evo in entry.get("evolutions", []):
        evo_types = evo.get("types", ["Unknown"])
        if "Unknown" in evo_types:
            e_name = evo["evolution"]
            e_data = get_best_data(e_name, cache_data)
            if e_data:
                evo["types"] = e_data.get("types", ["Unknown"])
                evo["bst"] = e_data.get("bst", evo.get("bst", 400))
                updated_count += 1

with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(json_data, f, indent=2)

print(f"Restored types/BST for {updated_count} entries.")
