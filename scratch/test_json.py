import json
import os
import re

# Mock the function from build_evos.py
def has_forward_vanilla_evolution(name):
    # This is a simplified version for debugging
    # In the real script, it checks a vanilla_evos list
    return True 

path = "random_bst_evolutions.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total entries in JSON: {len(data)}")
print(f"Is 'Growlithe' in JSON? {'Growlithe' in data}")
print(f"Is 'Pikachu' in JSON? {'Pikachu' in data}")
print(f"Is 'Bulbasaur' in JSON? {'Bulbasaur' in data}")
