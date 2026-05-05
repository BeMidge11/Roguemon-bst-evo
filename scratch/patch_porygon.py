import json
import os

path = r"c:\Users\benmi\Downloads\Roguemon-bst-evo-main\Roguemon-bst-evo-main\random_bst_evolutions.json"

if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    count = 0
    # Search all starters and their evolutions
    for starter, sdata in data.items():
        # Also check the starter itself if it's Porygon
        if starter == "Porygon" and sdata.get("base_bst") != 395:
            sdata["base_bst"] = 395
            count += 1
            
        for evo in sdata.get("evolutions", []):
            name = evo.get("evolution")
            if name == "Porygon" and evo.get("bst") != 395:
                evo["bst"] = 395
                evo["evolution_level"] = 39
                count += 1
            elif name == "Porygon2" and evo.get("bst") != 515:
                evo["bst"] = 515
                evo["evolution_level"] = 51
                count += 1
            elif name == "Porygon-Z" and evo.get("bst") != 535:
                evo["bst"] = 535
                evo["evolution_level"] = 53
                count += 1
                
    if count > 0:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"Successfully corrected {count} Porygon-line entries.")
    else:
        print("No incorrect Porygon entries found in JSON.")
else:
    print("JSON file not found.")
