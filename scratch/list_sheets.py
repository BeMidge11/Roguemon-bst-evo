import pandas as pd
import os

xlsx_path = r"c:\Users\benmi\Downloads\Roguemon-bst-evo-main\Roguemon-bst-evo-main\Roguemon Rankings.xlsx"

if os.path.exists(xlsx_path):
    xl = pd.ExcelFile(xlsx_path)
    print(f"Sheet names: {xl.sheet_names}")
else:
    print("Excel file not found.")
