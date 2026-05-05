import json

JSON_FILE = "random_bst_evolutions.json"
STARTER_FILE = "starter_rankings.json"

with open(JSON_FILE, "r", encoding="utf-8") as f:
    json_data = json.load(f)
with open(STARTER_FILE, "r", encoding="utf-8") as f:
    starters = json.load(f)

starter_names = set(s["name"] for s in starters)

# These are the ones we explicitly want to keep OUT of BST/10
pollution_list = ["Frillish", "Sneasel", "Sneasel H", "Pumpkaboo", "Pumpkaboo L", "Pumpkaboo S", "Pumpkaboo XL"]

updated_count = 0
for name in json_data:
    # Rule 1: If it's a ranked starter, it's 'injected' (hidden from BST/10)
    if name in starter_names:
        json_data[name]["injected"] = True
        updated_count += 1
    
    # Rule 2: Explicitly hide the pollution list even if they weren't in rankings
    if name in pollution_list or name.startswith("Pumpkaboo"):
        json_data[name]["injected"] = True

# Rule 3: There might be some starters the user actually WANTS in BST/10.
# Based on the user's feedback ("some starters are in there but not all"),
# we'll assume the "classic" ones like Charmander/Bulbasaur/etc are NOT what they meant
# by 'polluted' unless they say otherwise. 
# But to be safe and "perfect", we'll hide ALL 372 and let the user tell us 
# which ones to 'un-hide' if they notice a missing favorite.

with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(json_data, f, indent=2)

print(f"Secured BST/10 list by flagging {updated_count} starters as injected/hidden.")
