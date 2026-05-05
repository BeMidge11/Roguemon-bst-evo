import json
import requests
import os
import time

DATA_FILE = "random_bst_evolutions.json"
CACHE_FILE = "pokemon_data_cache.json"
POKEAPI = "https://pokeapi.co/api/v2/pokemon"

# Load existing data
with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# Load cache if exists
cache = {}
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        cache = json.load(f)

# Collect all unique evolutions
unique_evos = set()
for starter in data.values():
    for evo in starter["evolutions"]:
        unique_evos.add(evo["evolution"])

print(f"Found {len(unique_evos)} unique evolutions to process.")

def normalize_name(name):
    # Basic normalization similar to build_evos.py
    n = name.lower().replace(" ", "-").replace(".", "").replace("'", "")
    # Add common form mappings if needed
    if n == "floettee": return "floette-eternal"
    if n == "eeveep": return "eevee-starter"
    if n == "pikachup": return "pikachu-starter"
    return n

# Fetch types
count = 0
for name in unique_evos:
    if name in cache and "types" in cache[name]:
        continue
    
    slug = normalize_name(name)
    try:
        r = requests.get(f"{POKEAPI}/{slug}", timeout=10)
        if r.status_code == 200:
            res = r.json()
            types = [t["type"]["name"].capitalize() for t in res["types"]]
            if name not in cache: cache[name] = {}
            cache[name]["types"] = types
            count += 1
            if count % 50 == 0:
                print(f"Fetched {count} types...")
        else:
            print(f"Failed to fetch {name} ({slug})")
    except Exception as e:
        print(f"Error fetching {name}: {e}")
    
    # Save cache periodically
    if count % 20 == 0:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2)
    
    time.sleep(0.05) 

# Save cache
with open(CACHE_FILE, "w", encoding="utf-8") as f:
    json.dump(cache, f, indent=2)

# Patch the data
print("Patching JSON data...")
for starter in data.values():
    for evo in starter["evolutions"]:
        name = evo["evolution"]
        if name in cache and "types" in cache[name]:
            evo["types"] = cache[name]["types"]
        else:
            evo["types"] = ["Unknown"]

# Save patched data
with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("Done! All evolutions now have types.")
