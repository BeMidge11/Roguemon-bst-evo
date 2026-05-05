import json
import os

path = r"c:\Users\benmi\Downloads\Roguemon-bst-evo-main\Roguemon-bst-evo-main\random_bst_evolutions.json"

if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    found = []
    # Check top level
    if "Porygon" in data:
        found.append(f"Top level Porygon: {data['Porygon'].get('base_bst')}")
    
    # Check evolutions
    for starter, sdata in data.items():
        for evo in sdata.get("evolutions", []):
            if evo.get("evolution") == "Porygon":
                found.append(f"Evolution of {starter}: Porygon with BST {evo.get('bst')}")
                if len(found) > 10: break
        if len(found) > 10: break
                
    if found:
        print("\n".join(found))
    else:
        print("No 'Porygon' found in JSON.")
else:
    print("JSON file not found.")
