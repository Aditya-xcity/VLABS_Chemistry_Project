Q# Backend/main.py
# VLabs Backend - Python Version
# Name    : ADITYA BHARDWAJ
# Section : D2
# Roll No : 08
# Course  : B TECH
# Branch  : CSE


#------------sari import kari files----------------
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import pandas as pd
import os


#-----------flask app ko start kar dia
#----Enables CORS for cross-origin requests (so JS frontend can fetch data freely).
app = Flask(__name__)
CORS(app)

print("Starting VLABS Server...")

# Elements pick up kiye Excel sey
try:
    elements_df = pd.read_excel("Data/Elements.xlsx")
    elements = [{"symbol": str(row["Symbol"]).strip(), "name": str(row["Name"]).strip()} 
                #Then it loops through rows to make a clean list of dictionaries:
                for index, row in elements_df.iterrows()]
    print(f" Loaded {len(elements)} elements from Excel")
except Exception as e:
    print(f" Error loading Elements.xlsx: {e}")
    elements = []

# Load Reactions from Text File
reaction_map = {}
try:
    reactions_file = "Backend/reactions.txt"
    reaction_count = 0
    
    with open(reactions_file, 'r', encoding='utf-8') as file:
        for line_number, line in enumerate(file, 1):
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
                
            try:
                # Parse the line: Element1,Element2,Formula;IUPAC Name;Common Name
                parts = line.split(',')
                if len(parts) >= 3:
                    el1 = parts[0].strip()
                    el2 = parts[1].strip()
                    products_str = ','.join(parts[2:])  # Rejoin in case there are commas in products
                    products = [p.strip() for p in products_str.split(';') if p.strip()]
                    
                    if len(products) >= 3:
                        # Create both orders for the reaction
                        reaction_map[(el1, el2)] = products
                        reaction_map[(el2, el1)] = products
                        reaction_count += 1
                        print(f" Loaded: {el1} + {el2} → {products[0]}")
                    else:
                        print(f" Line {line_number}: Invalid products format")
                else:
                    print(f"Line {line_number}: Invalid format - {line}")
                    
            except Exception as e:
                print(f"error parsing line {line_number}: {e}")
                continue
    
    print(f" Successfully loaded {reaction_count} reactions from text file")
    print(f" Total reaction mappings: {len(reaction_map)}")
    
    # Show some sample reactions
    print("\n Sample reactions loaded:")
    sample_keys = list(reaction_map.keys())[:5]
    for key in sample_keys:
        print(f"   {key} → {reaction_map[key][0]}")
        
except Exception as e:
    print(f" Error loading reactions.txt: {e}")
    print("Make sure Backend/reactions.txt exists with the correct format")

# Route to serve frontend
@app.route("/")
def index():
    return render_template("index.html")

# API to get elements
@app.route("/get_elements")
def get_elements():
    return jsonify(elements)

# API to get reaction products
@app.route("/get_reaction")
def get_reaction():
    el1 = request.args.get("el1", "").strip()
    el2 = request.args.get("el2", "").strip()
    
    print(f" Reaction request: {el1} + {el2}")
    print(f" Looking for keys: ({el1}, {el2}) and ({el2}, {el1})")
    
    if not el1 or not el2:
        return jsonify({
            "type": "error",
            "reactants": [el1, el2],
            "products": ["Please select two elements"]
        })
    
    # Try both orders
    key1 = (el1, el2)
    key2 = (el2, el1)
    
    if key1 in reaction_map:
        products = reaction_map[key1]
        print(f" FOUND REACTION: {products}")
        return jsonify({
            "type": "binary", 
            "reactants": [el1, el2],
            "products": products
        })
    elif key2 in reaction_map:
        products = reaction_map[key2]
        print(f" FOUND REACTION: {products}")
        return jsonify({
            "type": "binary", 
            "reactants": [el1, el2],
            "products": products
        })
    
    print(f" NO REACTION FOUND for {el1} + {el2}")
    print(f"   Available reactions: {list(reaction_map.keys())}")
    return jsonify({
        "type": "no_reaction",
        "reactants": [el1, el2],
        "products": ["No reaction found between these elements"]
    })

@app.route("/debug")
def debug():
    """Debug endpoint to see what's loaded"""
    return jsonify({
        "status": "server_running",
        "elements_loaded": len(elements),
        "reactions_loaded": len(reaction_map),
        "available_elements": [el["symbol"] for el in elements[:10]],
        "available_reactions": [f"{k[0]}+{k[1]}" for k in list(reaction_map.keys())[:10]]
    })

@app.route("/test_reactions")
def test_reactions():
    """Test some common reactions"""
    test_cases = [
        ("H", "O"),
        ("Na", "Cl"),
        ("C", "O"),
        ("N", "H"),
        ("Mg", "O")
    ]
    
    results = []
    for el1, el2 in test_cases:
        key1 = (el1, el2)
        key2 = (el2, el1)
        found = key1 in reaction_map or key2 in reaction_map
        products = reaction_map.get(key1, reaction_map.get(key2, ["NOT FOUND"]))
        
        results.append({
            "elements": f"{el1} + {el2}",
            "found": found,
            "products": products
        })
    
    return jsonify(results)

if __name__ == "__main__":
    print("\n📡 Server running on: http://127.0.0.1:5000")
    print("🔬 Test URLs:")
    print("   http://127.0.0.1:5000/")
    print("   http://127.0.0.1:5000/debug")
    print("   http://127.0.0.1:5000/test_reactions")
    print("   http://127.0.0.1:5000/get_reaction?el1=H&el2=O")
    print("\n KEEP THIS TERMINAL OPEN - Server is running here!")
    app.run(debug=True, port=5000, use_reloader=False)