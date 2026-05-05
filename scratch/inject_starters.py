import json
import os

# Load all necessary data
REVO_FILE = "revo12000.txt"
JSON_FILE = "random_bst_evolutions.json"
STARTER_FILE = "starter_rankings.json"
CACHE_FILE = "pokemon_data_cache.json"

def load_revo_data():
    raw_revo = {}
    if not os.path.exists(REVO_FILE): return {}
    with open(REVO_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if " -> " not in line: continue
            parts = line.split(" -> ")
            name = parts[0].strip()
            evo_list = []
            evos_raw = parts[1].strip().split("), (")
            for er in evos_raw:
                er = er.replace("(", "").replace(")", "")
                if "," not in er: continue
                e_parts = er.rsplit(",", 1)
                e_name = e_parts[0].strip()
                weight = int(e_parts[1].strip())
                evo_list.append((e_name, weight))
            raw_revo[name] = evo_list
    return raw_revo

def get_bst_types(name, cache, data):
    # Try to find in existing JSON data first (most reliable)
    if name in data:
        return data[name].get("base_bst"), data[name].get("types", [])
    # Check cache
    # Need to handle slugs
    slug = name.lower().replace(" ", "-")
    if slug in cache:
        return cache[slug].get("bst"), cache[slug].get("types", [])
    return 400, ["Unknown"] # Fallback

def normalize_for_revo(name):
    # Convert 'Growlithe H' to 'Growlitheh', 'Zorua H' to 'Zoruah', etc.
    if name.endswith(" H"): return name.replace(" H", "h")
    if name.endswith(" G"): return name.replace(" G", "g")
    if name.endswith(" A"): return name.replace(" A", "a")
    if name.endswith(" P"): return name.replace(" P", "p")
    return name

# Main logic
revo_data = load_revo_data()
with open(JSON_FILE, "r", encoding="utf-8") as f:
    json_data = json.load(f)
with open(STARTER_FILE, "r", encoding="utf-8") as f:
    starters = json.load(f)
with open(CACHE_FILE, "r", encoding="utf-8") as f:
    cache_data = json.load(f)

count = 0
for s in starters:
    orig_name = s["name"]
    revo_name = normalize_for_revo(orig_name)
    
    # If it's already in the JSON AND it's NOT marked as injected, 
    # it's part of the 'perfect' list. Leave it alone.
    if orig_name in json_data and not json_data[orig_name].get("injected"):
        continue
    
    if revo_name in revo_data:
        # Build the entry
        evos = revo_data[revo_name]
        total_w = sum(w for _, w in evos)
        
        bst, types = get_bst_types(revo_name, cache_data, json_data)
        
        evolutions = []
        for e_name, w in evos:
            e_bst, e_types = get_bst_types(e_name, cache_data, json_data)
            evolutions.append({
                "evolution": e_name,
                "bst": e_bst,
                "types": e_types,
                "evolution_level": max(1, (e_bst // 10)),
                "probability": w / total_w
            })
            
        json_data[orig_name] = {
            "base_bst": bst,
            "rule": "bst/10",
            "forced": False,
            "injected": True, # Mark as injected so we can filter out of BST/10 tab
            "types": types,
            "evolutions": evolutions
        }
        count += 1

if count > 0:
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2)
    print(f"Successfully injected {count} starters into the evolution data.")
else:
    print("No missing starters found that were available in revo12000.txt.")
