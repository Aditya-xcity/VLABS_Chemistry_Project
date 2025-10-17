# check_excel_structure.py
import pandas as pd
import os

def check_file_structure():
    print("🔍 Checking Excel file structure...")
    
    # Check Elements.xlsx
    try:
        elements_path = "Data/Elements.xlsx"
        if os.path.exists(elements_path):
            print(f"\n✅ Elements.xlsx exists at: {elements_path}")
            elements_df = pd.read_excel(elements_path)
            print(f"   Shape: {elements_df.shape}")
            print(f"   Columns: {list(elements_df.columns)}")
            print(f"   First 3 rows:")
            print(elements_df.head(3))
        else:
            print(f"❌ Elements.xlsx not found at: {elements_path}")
    except Exception as e:
        print(f"❌ Error reading Elements.xlsx: {e}")
    
    # Check Result.xlsx
    try:
        results_path = "Backend/Result.xlsx"
        if os.path.exists(results_path):
            print(f"\n✅ Result.xlsx exists at: {results_path}")
            results_df = pd.read_excel(results_path)
            print(f"   Shape: {results_df.shape}")
            print(f"   Columns: {list(results_df.columns)}")
            print(f"   First 3 rows:")
            print(results_df.head(3))
            
            # Check specific columns
            if "Element1" in results_df.columns:
                print(f"   Element1 sample values: {results_df['Element1'].head(5).tolist()}")
            if "Element2" in results_df.columns:
                print(f"   Element2 sample values: {results_df['Element2'].head(5).tolist()}")
            if "Element3" in results_df.columns:
                print(f"   Element3 sample values: {results_df['Element3'].head(5).tolist()}")
                
            # Find products column
            products_cols = [col for col in results_df.columns if 'product' in col.lower() or 'reaction' in col.lower()]
            print(f"   Possible products columns: {products_cols}")
            if products_cols:
                print(f"   Products sample: {results_df[products_cols[0]].head(3).tolist()}")
                
        else:
            print(f"❌ Result.xlsx not found at: {results_path}")
    except Exception as e:
        print(f"❌ Error reading Result.xlsx: {e}")

if __name__ == "__main__":
    check_file_structure()