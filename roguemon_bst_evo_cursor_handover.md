# Roguemon BST Evolution Builder — Handover Document

## Purpose of This Document

This document provides a clear technical handover for development of the **Roguemon BST Evolution Builder** project. The project has been updated to use **`RoguemonRevoData.lua`** directly in place of the legacy `revo12000.txt`.

The build is fast, deterministic, offline, and provides 100% coverage across all 567 Roguemon starters and their random evolution pools.

---

# Project Overview

This repository builds an evolution dataset mapping Pokémon evolutions based on Base Stat Total (BST) relationships derived from the Roguemon engine source data:

```
RoguemonRevoData.lua
```

The build pipeline:

```
RoguemonRevoData.lua (567 starters, 1151 species IDs)
      ↓
Species ID Resolution (species_data.json mapped to pokeemerald-expansion Species enum)
      ↓
Base BST & Evolution Calculations (BST / 10 levels, type combinations, probability)
      ↓
random_bst_evolutions.json
```

A GitHub Actions CI workflow (`.github/workflows/build-evos.yml`) automatically rebuilds data whenever `RoguemonRevoData.lua` or build scripts change.

---

# Architecture & Migration from revo12000.txt

### Legacy Issues with `revo12000.txt`
1. Misspellings and ROM shorthand names (`Corvknight`, `Kilowattrl`, `Fluttrmane`, `Roarinmoon`).
2. Suffix duplicates (`Kirlia1`, `Kirlia2`, `Dewott1`, `Dewott2`).
3. Form abbreviations (`wooperp`, `taurospw`, `oinkolognf`).
4. Heavy reliance on flaky external API calls to PokéAPI, resulting in missing starters and API rate limits.

### Resolution with `RoguemonRevoData.lua`
1. `RoguemonRevoData.lua` contains clean starter entries (`[id] = { -- Name }`) and exact percentage evolutions (`{ id = evo_id, perc = ... }`).
2. The species IDs map 1:1 with `pokeemerald-expansion`'s `Species` enum and Pokémon Showdown dataset.
3. `species_data.json` provides an instant, offline O(1) lookup for all 1151 species IDs (Name, BST, Types, Evolution Level, Sprite Slug).
4. Build time dropped from hours to **< 0.1s**, with **100.00% coverage** and **0 failed lookups**.

---

# Key Files

- **`RoguemonRevoData.lua`**: Source evolution data for Roguemon.
- **`species_data.json`**: Pre-resolved lookup table mapping species IDs to Showdown names, BSTs, and types.
- **`build_evos.py`**: Automated build script converting `RoguemonRevoData.lua` to `random_bst_evolutions.json`.
- **`random_bst_evolutions.json`**: Generated JSON dataset consumed by the web app.
- **`failed_lookups.json`**: Diagnostics logging any failed Pokémon or evolution forms (currently 0).
- **`app.js` & `index.html`**: Front-end interactive calculator with search, animated sprites, level filters, and charts.
- **`.github/workflows/build-evos.yml`**: CI workflow triggered on updates to `RoguemonRevoData.lua`.

---

# Running the Build

To rebuild the evolution table:

```bash
python build_evos.py
```

Expected output:
```
Using source data: RoguemonRevoData.lua
Building BST-based random evolution table...
Building evolution table from Lua source: RoguemonRevoData.lua

===== SUMMARY =====
Starters seen:  567
Starters kept: 567
BST lookups:   567
Failed starters: 0
Failed evolution forms: 0
Total failures: 0
Coverage: 100.00%
Time:          0.06s
===================
```
