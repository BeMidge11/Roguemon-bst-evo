import pandas as pd
import json
import os

xlsx_path = r"c:\Users\benmi\Downloads\Roguemon-bst-evo-main\Roguemon-bst-evo-main\Roguemon Rankings.xlsx"
json_output = r"c:\Users\benmi\Downloads\Roguemon-bst-evo-main\Roguemon-bst-evo-main\starter_rankings.json"

if os.path.exists(xlsx_path):
    try:
        # Read specifically the 'Sprites' sheet
        df = pd.read_excel(xlsx_path, sheet_name='Sprites')
        
        # In the Sprites sheet, names are usually in the first column or labeled 'Species'
        name_col = None
        for col in df.columns:
            c_low = str(col).lower()
            if 'species' in c_low or 'pokemon' in c_low or 'name' in c_low:
                name_col = col
                break
        
        if name_col is None:
            name_col = df.columns[0]
            
        print(f"Using column '{name_col}' from 'Sprites' sheet")
        
        all_starters = []
        for _, row in df.iterrows():
            name = str(row[name_col]).strip()
            # Basic validation to ensure it's a name
            if not name or name == 'nan' or len(name) < 2:
                continue
            if name.lower() in ['date', 'species', 'pokemon', 'name', 'sprites']:
                continue
            if '00:00:00' in name:
                continue
                
            clean_name = name.split('(')[0].strip()
            all_starters.append({
                "name": clean_name,
                "type_sheet": "Starter"
            })
            
        with open(json_output, "w", encoding="utf-8") as f:
            json.dump(all_starters, f, indent=2)
            
        print(f"Successfully extracted {len(all_starters)} starters from 'Sprites' to {json_output}")
    except Exception as e:
        print(f"Error reading Excel: {e}")
else:
    print("Excel file not found.")
