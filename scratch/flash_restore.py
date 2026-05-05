import json
import os

JSON_FILE = "random_bst_evolutions.json"
SOURCE_FILE = "revo12000.txt"

if not os.path.exists(SOURCE_FILE):
    print("revo12000.txt not found! Falling back to BST rules.")
    # Fallback to BST/Forced rules if the txt is missing
    source_names = None
else:
    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        # The first name on each line of revo12000.txt is a valid BST/10 starter
        source_names = set(line.split()[0] for line in f if line.strip())

with open(JSON_FILE, "r", encoding="utf-8") as f:
    json_data = json.load(f)

print(f"Current entries: {len(json_data)}")

cleaned_data = {}
for name, entry in json_data.items():
    # Only keep it if it was in the original revo list OR fits the strict rules
    is_original = (source_names is None) or (name in source_names)
    is_valid_bst = entry.get("base_bst", 0) <= 450
    is_not_forced = not entry.get("forced", False)
    
    if is_original and is_valid_bst and is_not_forced:
        cleaned_data[name] = entry

with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(cleaned_data, f, indent=2)

print(f"Restored entries: {len(cleaned_data)}")
print("Flash Restore Complete. File size should be drastically reduced.")
