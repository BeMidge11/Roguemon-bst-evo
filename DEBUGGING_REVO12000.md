## Debugging revo12000 Display Issues

### Problem
Pokémon from the revo12000.txt file aren't showing up in the app, likely due to:
1. **Name mismatches** between revo12000 data and PokéAPI
2. **Parsing errors** in the build process
3. **Failed API lookups** that silently skip entries
4. **Frontend rendering issues** for Pokémon without valid evolutions

---

## Investigation Steps

### 1. Check the Build Process
Run the updated `build_evos.py`:
```bash
python build_evos.py
```

This will now generate a `failed_lookups.json` file showing:
- Which starters failed to load their base BST
- Which evolution forms had API lookup errors
- Exact error messages from PokéAPI

### 2. Review Failed Lookups
The `failed_lookups.json` file shows problematic Pokémon names. Common issues:
- **Typos in revo12000.txt**: e.g., "Gengarm" vs "gengar-mega"
- **Regional forms not found**: e.g., "Mudkip" (Hoenn-specific) might not have a form name in PokéAPI
- **Unrecognized names**: Romhacks sometimes create custom Pokémon names

### 3. Enhance NAME_ALIASES
The `build_evos.py` includes a comprehensive `NAME_ALIASES` dictionary. If you find unrecognized Pokémon:

1. **Check PokéAPI** for the exact form name:
   ```
   https://pokeapi.co/api/v2/pokemon/{name}
   ```

2. **Add to NAME_ALIASES**:
   ```python
   "RomhackName": "official-pokeapi-name",
   ```

Example: If revo12000 has "Mudkipp" but PokéAPI uses "mudkip":
```python
"Mudkipp": "mudkip",  # Typo fix
```

### 4. Frontend Filtering Issues
Check `app.js` line 50-53 for the `getValidEvos()` function:
```javascript
function getValidEvos() {
  const lvl = parseInt(currentLevelInput.value) || 1;
  return selectedPokemon.evolutions.filter(e => e.evolution_level > lvl);
}
```

**Problem**: If a Pokémon has NO valid evolutions (all evolution_level ≤ current level), it shows no results.

**Solution**: Add debug logging in your browser console:
```javascript
function selectPokemon(name) {
  input.value = name;
  suggestionsBox.hidden = true;
  selectedPokemon = DATA[name];
  console.log("Selected:", name);
  console.log("Data:", selectedPokemon);
  selectedLevel = null;
  render();
}
```

---

## Common Issues & Fixes

### Issue 1: Pokémon Not in Suggestions
**Cause**: The starter Pokémon name doesn't match the JSON output
**Fix**: Run build_evos.py and check `failed_lookups.json` for why it wasn't included

### Issue 2: Empty Evolution List
**Cause**: 
- All evolution forms from revo12000 had API lookup errors
- All evolution levels are ≤ current Pokémon level (use the level pills)

**Fix**: 
- Check `failed_lookups.json` → `failed_evolutions`
- Verify evolution names in NAME_ALIASES
- Increase the current level input to see higher-level evolutions

### Issue 3: Mismatched BST Values
**Cause**: revo12000.txt has Pokémon with different BSTs than official data
**Example**: A regional form might have tweaked stats in the romhack

**Fix**: 
1. Compare revo12000.txt data with actual BST values
2. If discrepancy is intentional, create a `bst_overrides.json` entry:
   ```json
   {
     "force_bst_starter": ["PokémonName"],
     "bst_overrides": {
       "PokémonName": 420
     }
   }
   ```

3. Modify `build_evos.py` to use overrides:
   ```python
   if starter in OVERRIDES.get("bst_overrides", {}):
       base_bst = OVERRIDES["bst_overrides"][starter]
   ```

---

## Step-by-Step Repair Process

1. **Clear previous build**:
   ```bash
   rm random_bst_evolutions.json failed_lookups.json
   ```

2. **Run the updated script**:
   ```bash
   python build_evos.py
   ```

3. **Open browser console** while viewing the app:
   - Press `F12` → Console tab
   - Try selecting a Pokémon from revo12000
   - Check for error messages

4. **Review `failed_lookups.json`** for patterns:
   - If many names are misspelled, create a name mapping
   - If API calls are rate-limited, add retry logic
   - If custom Pokémon don't exist in PokéAPI, create placeholder entries

5. **Update NAME_ALIASES** with any missing mappings:
   ```python
   NAME_ALIASES.update({
       "BadName1": "good-name-1",
       "BadName2": "good-name-2",
   })
   ```

6. **Rebuild**:
   ```bash
   python build_evos.py
   ```

7. **Test in browser** and refresh to see updated data

---

## Additional Debugging

### Check All Pokémon in Output
```bash
python -c "import json; data = json.load(open('random_bst_evolutions.json')); print(f'Total: {len(data)}'); print('\\n'.join(sorted(data.keys())[:20]))"
```

### Verify Specific Pokémon
```bash
python -c "import json; data = json.load(open('random_bst_evolutions.json')); print(json.dumps(data.get('YourPokémonName', 'NOT FOUND'), indent=2))"
```

### Test API Directly
```bash
curl "https://pokeapi.co/api/v2/pokemon/your-pokemon-name"
```

---

## If All Else Fails

1. **Manually patch** `random_bst_evolutions.json` with missing entries
2. **Create a mapping script** to convert all revo12000 names to PokéAPI format
3. **Use fuzzy matching** to auto-correct name mismatches
4. **Contact PokéAPI support** if certain forms aren't available

---

## Files to Modify
- `build_evos.py` - Main build script (updated with better error handling)
- `NAME_ALIASES` dict - Add missing name mappings
- `bst_overrides.json` - Override BST values if needed
- `random_bst_evolutions.json` - Final output (regenerated after fixes)
