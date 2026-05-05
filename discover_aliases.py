

import os
os.environ.pop("SSLKEYLOGFILE", None)
import re
import time
import requests
from functools import lru_cache

# =========================
# CONFIG
# =========================

EVO_FILE = "revo12000.txt"
OUTPUT_ALIASES = "discovered_aliases.json"
OUTPUT_UNRESOLVED = "unresolved_names.txt"

POKEAPI = "https://pokeapi.co/api/v2"
REQUEST_DELAY = 0.05   # be nice to the API

# =========================
# HELPERS
# =========================

def strip_slot(name: str) -> str:
    """Remove trailing slot numbers (Kirlia1 -> Kirlia)."""
    return re.sub(r"\d+$", "", name)

def base_normalize(name: str) -> str:
    """Minimal safe normalization."""
    n = name.lower().strip()
    n = n.replace("’", "").replace("'", "")
    n = n.replace(".", "").replace(":", "")
    n = n.replace("♀", "-f").replace("♂", "-m")
    n = n.replace(" ", "-")
    n = re.sub(r"-+", "-", n)
    return n

def candidate_forms(name: str):
    """
    Generate reasonable PokéAPI candidates.
    Order matters — first hit wins.
    """
    n = base_normalize(strip_slot(name))

    candidates = [
        n,
        n + "-mega",
        n + "-alola",
        n + "-galar",
        n + "-hisui",
        n + "-paldea",
        n + "-therian",
        n + "-origin",
        n + "-10",
        n + "-complete",
    ]

    # Common ROM shorthand endings
    if n.endswith("m"):
        candidates.append(n[:-1] + "-mega")
    if n.endswith("g"):
        candidates.append(n[:-1] + "-galar")
    if n.endswith("h"):
        candidates.append(n[:-1] + "-hisui")

    return list(dict.fromkeys(candidates))  # dedupe, preserve order

@lru_cache(maxsize=None)
def exists_in_pokeapi(name: str) -> bool:
    r = requests.get(f"{POKEAPI}/pokemon/{name}")
    time.sleep(REQUEST_DELAY)
    return r.ok

# =========================
# PARSE EVO FILE
# =========================

def extract_all_names(path):
    starters = set()
    evos = set()

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if "->" not in line:
                continue

            starter, rest = line.split("->", 1)
            starters.add(strip_slot(starter.strip()))

            for evo in re.findall(r"\(([^,]+),", rest):
                evos.add(strip_slot(evo.strip()))

    return starters | evos

# =========================
# MAIN DISCOVERY
# =========================

def main():
    names = extract_all_names(EVO_FILE)

    aliases = {}
    unresolved = []

    print(f"Scanning {len(names)} unique species names...\n")

    for i, raw in enumerate(sorted(names), 1):
        found = False

        for candidate in candidate_forms(raw):
            if exists_in_pokeapi(candidate):
                aliases[raw] = candidate
                found = True
                break

        if not found:
            unresolved.append(raw)

        if i % 25 == 0:
            print(f"[{i}/{len(names)}] checked")

    # =========================
    # OUTPUT
    # =========================

    import json
    with open(OUTPUT_ALIASES, "w", encoding="utf-8") as f:
        json.dump(aliases, f, indent=2, ensure_ascii=False)

    with open(OUTPUT_UNRESOLVED, "w", encoding="utf-8") as f:
        for name in sorted(unresolved):
            f.write(name + "\n")

    print("\n===== DONE =====")
    print(f"Aliases found:   {len(aliases)}")
    print(f"Still unresolved: {len(unresolved)}")
    print("================")

if __name__ == "__main__":
    main()
