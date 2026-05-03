import json
import shutil
from collections import defaultdict

DATA_FILE = "random_bst_evolutions.json"
BACKUP_FILE = DATA_FILE + ".bak"


def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def write_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def backup_file():
    shutil.copy2(DATA_FILE, BACKUP_FILE)
    print(f"✔ Backup created: {BACKUP_FILE}")


def collect_missing_bst(data):
    """
    Returns:
        missing: dict[str, list[dict]]
        key = pokemon name
        value = list of evo dict references to patch
    """
    missing = defaultdict(list)

    for starter, entry in data.items():
        for evo in entry.get("evolutions", []):
            if evo.get("bst") is None:
                missing[evo["evolution"]].append(evo)

    return missing


def prompt_for_bst(pokemon, index, total):
    while True:
        raw = input(
            f"\n[{index}/{total}] Missing BST for '{pokemon}' "
            f"(enter number, blank = skip): "
        ).strip()

        if raw == "":
            return None

        if raw.isdigit():
            return int(raw)

        print("❌ Please enter a valid integer or press Enter to skip.")


def main():
    print("=== BST NULL FIXER ===")

    data = load_data()
    missing = collect_missing_bst(data)

    if not missing:
        print("✔ No missing BST values found. Nothing to do.")
        return

    print(f"Found {len(missing)} Pokémon with missing BSTs.")

    backup_file()

    updated = 0
    skipped = 0

    total = len(missing)

    for i, (pokemon, entries) in enumerate(missing.items(), 1):
        bst = prompt_for_bst(pokemon, i, total)

        if bst is None:
            skipped += 1
            print(f"↷ Skipped {pokemon}")
            continue

        evo_level = bst // 10

        for evo in entries:
            evo["bst"] = bst
            evo["evolution_level"] = evo_level

        updated += 1
        print(f"✔ Updated {pokemon} in {len(entries)} place(s)")

    write_data(data)

    print("\n=== DONE ===")
    print(f"Updated Pokémon: {updated}")
    print(f"Skipped Pokémon: {skipped}")
    print(f"Output written to: {DATA_FILE}")


if __name__ == "__main__":
    main()
