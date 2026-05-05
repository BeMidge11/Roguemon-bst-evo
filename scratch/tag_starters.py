import json
import os

JSON_FILE = "random_bst_evolutions.json"
STARTER_FILE = "starter_rankings.json"

with open(JSON_FILE, "r", encoding="utf-8") as f:
    json_data = json.load(f)
with open(STARTER_FILE, "r", encoding="utf-8") as f:
    starters = json.load(f)

starter_names = set(s["name"] for s in starters)

# Pokémon we want to KEEP in the perfect BST/10 list (the original 95 or so)
# These are ones that were NOT added by my injection.
# I'll check which ones don't have the 'injected' flag yet.

# Wait, if I already ran the injection once, they might all be merged.
# But I can identify the "removed" ones like Frillish, Sneasel, etc.
removed_list = ["Frillish", "Sneasel", "Sneasel H", "Pumpkaboo", "Pumpkaboo L", "Pumpkaboo S", "Pumpkaboo XL"]

count = 0
for name in json_data:
    # If it's a starter AND it's in the removed list, or it's just 'new'
    # we mark it as injected.
    if name in starter_names:
        # If it was one of the ones the user explicitly wanted out of BST/10
        if name in removed_list or name.startswith("Pumpkaboo"):
            json_data[name]["injected"] = True
            count += 1
        # Also, if it was part of the 315 I added, it should have the flag.
        # I'll assume anything that isn't one of the 'classic' 95 is injected.
        # But I don't have the 95 list.
        # Actually, the user said "some starters ARE in there".
        
# Let's just mark ALL starters as 'injected' for now, 
# and then I'll update the app to ONLY hide the 'injected' ones.
# But wait, the user wants SOME starters to show.

# I will use a simple heuristic: 
# If it's a starter, it's 'injected' UNLESS it was already in the 
# 'perfect' version.
# I'll look at the file size of a previous version if I had one? No.

# I'll just mark the "removed" ones as injected for now.
for name in removed_list:
    if name in json_data:
        json_data[name]["injected"] = True

with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(json_data, f, indent=2)
print(f"Marked {count} suspicious starters as injected.")
