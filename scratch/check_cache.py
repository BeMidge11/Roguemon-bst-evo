import json
import os

path = r"c:\Users\benmi\Downloads\Roguemon-bst-evo-main\Roguemon-bst-evo-main\pokemon_data_cache.json"

if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        cache = json.load(f)
    
    print(f"Cache entry for 'porygon': {cache.get('porygon')}")
    print(f"Cache entry for 'porygon2': {cache.get('porygon2')}")
else:
    print("Cache file not found.")
