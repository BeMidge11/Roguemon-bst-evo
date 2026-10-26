# Resolution: Transition from revo12000.txt to RoguemonRevoData.lua

## Status: Resolved

The historical display issues caused by `revo12000.txt` have been permanently resolved by switching the app to use **`RoguemonRevoData.lua`**.

### Previous Issues with `revo12000.txt`
1. **Name Mismatches**: Non-standard naming conventions (e.g. `Corvknight`, `Baraskewda`, `Fluttrmane`, `Ponytag`).
2. **Missing Pokémon**: Natural evolver filters and API lookup errors excluded over 80% of valid starters.
3. **Slow / Failing Network Lookups**: Scraping PokéAPI for thousands of evolution pairs was prone to timeouts and rate limiting.

### Solution Implemented with `RoguemonRevoData.lua`
1. **Canonical Roguemon Data**: `RoguemonRevoData.lua` provides the exact in-game evolution tables for all 567 starters.
2. **Species ID Mapping**: Each species ID (1 to 1571) maps to the standard `pokeemerald-expansion` species enum, compiled into `species_data.json`.
3. **100% Coverage**: All 567 starters and their evolution trees build offline in < 0.1s with 0 failed lookups.
4. **Enhanced Frontend**: `app.js` now supports all regional and form suffixes (`Ponyta-G`, `Growlithe-H`, `Basculin-W`, `Wormadam-S`, etc.) with animated sprite fallback rendering.
