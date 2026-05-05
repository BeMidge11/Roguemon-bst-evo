import json

JSON_FILE = "random_bst_evolutions.json"

with open(JSON_FILE, "r", encoding="utf-8") as f:
    json_data = json.load(f)

print(f"Original line count roughly: {sum(len(str(v)) for v in json_data.values()) / 50}") # Rough estimate

for name in json_data:
    entry = json_data[name]
    if "evolutions" in entry:
        # Keep only the top 100 most probable evolutions
        # (This is plenty for a 10% chance sim and matches the original file's density)
        evos = entry["evolutions"]
        evos.sort(key=lambda x: x.get("probability", 0), reverse=True)
        entry["evolutions"] = evos[:100]

with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(json_data, f, indent=2)

print("Path Pruning Complete. JSON should be much smaller now.")
