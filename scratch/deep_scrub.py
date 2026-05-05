import json
import os

JSON_FILE = "random_bst_evolutions.json"

if not os.path.exists(JSON_FILE):
    print("File not found!")
    exit(1)

with open(JSON_FILE, "r", encoding="utf-8") as f:
    json_data = json.load(f)

print(f"Initial count: {len(json_data)} entries.")

# The "Perfect" Criteria:
# 1. BST must be 450 or under.
# 2. Must NOT have a natural vanilla evolution (forced: false).
# 3. Must NOT be one of the known 'polluters'.

blacklist = ["frillish", "sneasel", "pumpkaboo"]

cleaned_data = {}
for name, entry in json_data.items():
    # Only keep if it follows the BST/10 mode rules exactly
    is_low_bst = entry.get("base_bst", 0) <= 450
    is_not_forced = not entry.get("forced", False)
    is_not_blacklisted = not any(b in name.lower() for b in blacklist)
    
    if is_low_bst and is_not_forced and is_not_blacklisted:
        cleaned_data[name] = entry

with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(cleaned_data, f, indent=2)

print(f"Final count: {len(cleaned_data)} entries.")
print("JSON has been Deep Scrubbed.")
