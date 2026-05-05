import json
import os

path = r"c:\Users\benmi\Downloads\Roguemon-bst-evo-main\Roguemon-bst-evo-main\random_bst_evolutions.json"

if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Remove Sneasel, Frillish, and all Pumpkaboos
    to_remove = ["Sneasel", "Frillish", "Pumpkaboo", "Pumpkabool", "Pumpkaboos", "Pumpkaboox"]
    
    removed = []
    for p in to_remove:
        if p in data:
            del data[p]
            removed.append(p)
        
    if removed:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"Successfully removed: {', '.join(removed)}")
    else:
        print("Target Pokémon were not found in the JSON.")
else:
    print("JSON file not found.")
