import os
import re
import json
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
LUA_FILE = os.path.join(PARENT_DIR, "RoguemonRevoData.lua")
SPECIES_DATA_FILE = os.path.join(PARENT_DIR, "species_data.json")

TOTAL_RUNS = 12000

def load_species_data():
    if os.path.exists(SPECIES_DATA_FILE):
        with open(SPECIES_DATA_FILE, "r", encoding="utf-8") as f:
            return {int(k): v for k, v in json.load(f).items()}
    return {}

def parse_lua_revo_file(path):
    species_data = load_species_data()
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    starter_blocks = re.findall(r'\s*\[(\d+)\]\s*=\s*\{\s*--\s*(.+?)\s*\n(.*?)\n\s*\},', text, re.DOTALL)
    result = {}

    for sid_str, sname_hint, block in starter_blocks:
        starter_id = int(sid_str)
        starter_name = sname_hint.strip()
        s_info = species_data.get(starter_id, {})
        base_bst = s_info.get("bst", 300)
        types = s_info.get("types", ["Normal"])

        evo_matches = re.findall(r'\{\s*id\s*=\s*(\d+)\s*,\s*perc\s*=\s*([0-9.]+)\s*\}', block)
        processed = []
        for eid_str, perc_str in evo_matches:
            eid = int(eid_str)
            perc = float(perc_str)
            e_info = species_data.get(eid, {})
            ename = e_info.get("name", f"Species_{eid}")
            bst = e_info.get("bst", 400)
            etypes = e_info.get("types", ["Normal"])
            evo_lvl = e_info.get("evolution_level", max(1, bst // 10))

            processed.append({
                "evolution": ename,
                "bst": bst,
                "types": etypes,
                "evolution_level": evo_lvl,
                "probability": round(perc / 100.0, 6)
            })

        processed.sort(key=lambda x: (x["bst"] is None, x["bst"] if x["bst"] is not None else 0))
        result[starter_name] = {
            "base_bst": base_bst,
            "rule": "bst/10",
            "forced": False,
            "types": types,
            "evolutions": processed
        }

    return result

data = parse_lua_revo_file(LUA_FILE)
print(f"Total starters parsed: {len(data)}")
print(f"Sample starter 'Bulbasaur': {data.get('Bulbasaur')}")
