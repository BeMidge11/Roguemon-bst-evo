# Roguemon BST Evolution Builder — Cursor Handover Document

## Purpose of This Document

This document provides a clear technical handover for continuing development of the **Roguemon BST Evolution Builder** project using Cursor. It explains the current system, what is working, what is failing, and the exact next engineering steps required so the **end‑user tool accurately reflects data from `revo12000.txt`.**

The goal is stability, determinism, and full coverage of evolution data.

---

# Project Overview

This repository builds a dataset mapping Pokémon evolutions based on Base Stat Total (BST) relationships derived from a source file:

```
revo12000.txt
```

The build pipeline:

```
revo12000.txt
      ↓
name normalization
      ↓
BST lookup (API or dataset)
      ↓
evolution resolution
      ↓
random_bst_evolutions.json
```

A CI workflow automatically rebuilds data whenever inputs change.

---

# Current Status

## Infrastructure

Working:

- GitHub Actions workflow
- Automated build
- Commit + push from CI
- Failure logging
- Deterministic build execution

Files produced:

```
random_bst_evolutions.json
failed_lookups.json
```

The system builds successfully.

The remaining issues are **data normalization**, not infrastructure.

---

# Core Problem

Some Pokémon names from `revo12000.txt` do not resolve to valid BST entries.

These failures fall into predictable categories.

## Failure Categories

### 1) Numeric suffix variants

Examples:

```
Kirlia1
Kirlia2
Tyrogue1
Tyrogue2
Tyrogue3
```

These represent branching or form variants and should normalize to:

```
kirlia
tyrogue
```

---

### 2) Regional / form suffix shorthand

Examples:

```
wooperp
taurospw
oinkolognf
```

These encode forms such as:

```
p → paldea
w → water
f → female
```

---

### 3) Misspellings in source data

Examples:

```
Corvknight
Kilowattrl
Baraskewda
Fluttrmane
```

These require deterministic alias correction.

---

### 4) Unicode punctuation

Examples:

```
Farfetch’d
Sirfetch’d
Mime Jr.
```

These must normalize to API-safe names.

---

# System Architecture

## Key Files

```
build_evos.py
revo12000.txt
name_aliases.json
bst_overrides.json
random_bst_evolutions.json
failed_lookups.json
.github/workflows/build.yml
```

---

# Data Flow

```
INPUT
  revo12000.txt

PROCESS
  normalize_name()
  expand_forms()
  apply_aliases()
  lookup_bst()

OUTPUT
  random_bst_evolutions.json

LOGGING
  failed_lookups.json
```

---

# Required Normalization Pipeline

This pipeline must run in this exact order.

## Step 1 — Normalize Unicode

```
unicodedata.normalize("NFKD")
```

Fixes:

```
’ → '
```

---

## Step 2 — Lowercase

```
name = name.lower()
```

---

## Step 3 — Remove numeric suffix

```
re.sub(r"\\d+$", "", name)
```

---

## Step 4 — Remove punctuation

Remove:

```
.
'
’
```

---

## Step 5 — Expand form suffixes

Example mapping:

```
p → -paldea
f → -female
m → -male
w → -water
g → -galar
h → -hisui
a → -alola
```

---

## Step 6 — Apply alias corrections

```
ALIASES[name]
```

---

## Step 7 — BST lookup

Final normalized name must match dataset.

---

# Required Function

Cursor should implement or verify this function.

```python
import re
import unicodedata
import json

with open("name_aliases.json") as f:
    ALIASES = json.load(f)

FORM_MAP = {
    "p": "-paldea",
    "f": "-female",
    "m": "-male",
    "w": "-water",
    "g": "-galar",
    "h": "-hisui",
    "a": "-alola"
}


def normalize_name(name: str) -> str:
    name = unicodedata.normalize("NFKD", name)

    name = name.lower()

    name = re.sub(r"\\d+$", "", name)

    name = name.replace(".", "")
    name = name.replace("'", "")
    name = name.replace("’", "")

    if name and name[-1] in FORM_MAP:
        name = name[:-1] + FORM_MAP[name[-1]]

    name = ALIASES.get(name, name)

    return name
```

---

# Next Development Tasks

These are ordered by priority.

---

## Task 1 — Expand name_aliases.json

Goal:

Resolve all deterministic spelling errors.

Example entries:

```json
{
  "corvknight": "corviknight",
  "kilowattrl": "kilowattrel",
  "baraskewda": "barraskewda",
  "fluttrmane": "flutter-mane",
  "dudunsprce": "dudunsparce",
  "squawkbily": "squawkabilly"
}
```

---

## Task 2 — Add Coverage Metric

At end of build:

```python
coverage = success / total
print(f"Coverage: {coverage:.2%}")
```

---

## Task 3 — Enforce Coverage Threshold

Build must fail if coverage drops.

```python
if coverage < 0.98:
    raise RuntimeError("Coverage below threshold")
```

---

## Task 4 — Verify Output Matches Input

Ensure all starters from `revo12000.txt` exist in output.

```python
missing = set(revo_names) - set(output_names)

if missing:
    print("Missing entries:")
    for m in missing:
        print(m)
```

---

## Task 5 — Improve Failure Logging

Current logging is sufficient but should include counts.

Add:

```python
print("Total failures:", len(failed))
```

---

# CI Workflow Summary

Trigger:

```
push to main
```

Monitored files:

```
revo12000.txt
build_evos.py
name_aliases.json
bst_overrides.json
```

CI Steps:

```
checkout
setup python
install dependencies
run build
commit output
push
```

---

# Success Criteria

The system is considered complete when:

```
Coverage ≥ 99%

No missing starters

Build is deterministic

CI runs without manual fixes

End‑user tool output matches revo12000
```

---

# Non‑Goals

Do NOT:

- Rewrite the pipeline
- Replace the API
- Manually edit output JSON
- Change CI architecture

The system is already structurally correct.

---

# Optional Future Improvements

Not required immediately.

Possible upgrades:

- Cache API responses
- Parallel processing
- Fuzzy name matching fallback
- Dataset versioning
- Validation tests

---

# Quick Command Reference

Run locally:

```
python build_evos.py
```

Manual rebuild via GitHub:

```
Actions → Run workflow
```

---

# One‑Sentence Summary for Cursor

The system works; implement deterministic name normalization and alias mapping so every entry in `revo12000.txt` resolves to a valid BST and the generated evolution dataset fully reflects the source file.

