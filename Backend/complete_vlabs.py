# complete_vlabs.py
# COMPLETE VLABS SOLUTION - Everything in one file
# Name    : ADITYA BHARDWAJ
# Section : D2
# Roll No : 08
# Course  : B TECH
# Branch  : CSE

from flask import Flask, jsonify, request
import pandas as pd
import threading
import time
import webbrowser
import os

app = Flask(__name__)

# Manual elements data based on your Excel file
elements = [
    {"symbol": "H", "name": "Hydrogen"},
    {"symbol": "He", "name": "Helium"},
    {"symbol": "Li", "name": "Lithium"},
    {"symbol": "Be", "name": "Beryllium"},
    {"symbol": "B", "name": "Boron"},
    {"symbol": "C", "name": "Carbon"},
    {"symbol": "N", "name": "Nitrogen"},
    {"symbol": "O", "name": "Oxygen"},
    {"symbol": "F", "name": "Fluorine"},
    {"symbol": "Ne", "name": "Neon"},
    {"symbol": "Na", "name": "Sodium"},
    {"symbol": "Mg", "name": "Magnesium"},
    {"symbol": "Al", "name": "Aluminum"},
    {"symbol": "Si", "name": "Silicon"},
    {"symbol": "P", "name": "Phosphorus"},
    {"symbol": "S", "name": "Sulfur"},
    {"symbol": "Cl", "name": "Chlorine"},
    {"symbol": "Ar", "name": "Argon"},
    {"symbol": "K", "name": "Potassium"},
    {"symbol": "Ca", "name": "Calcium"},
    {"symbol": "Sc", "name": "Scandium"},
    {"symbol": "Ti", "name": "Titanium"},
    {"symbol": "V", "name": "Vanadium"},
    {"symbol": "Cr", "name": "Chromium"},
    {"symbol": "Mn", "name": "Manganese"},
    {"symbol": "Fe", "name": "Iron"},
    {"symbol": "Co", "name": "Cobalt"},
    {"symbol": "Ni", "name": "Nickel"},
    {"symbol": "Cu", "name": "Copper"},
    {"symbol": "Zn", "name": "Zinc"},
    {"symbol": "Ga", "name": "Gallium"},
    {"symbol": "Ge", "name": "Germanium"},
    {"symbol": "As", "name": "Arsenic"},
    {"symbol": "Se", "name": "Selenium"},
    {"symbol": "Br", "name": "Bromine"},
    {"symbol": "Kr", "name": "Krypton"}
]

# Manual reactions data based on your provided reactions
reaction_map = {
    # Binary reactions
    ("H", "O"): ["H₂O", "Dihydrogen Monoxide", "Water"],
    ("O", "H"): ["H₂O", "Dihydrogen Monoxide", "Water"],
    ("Na", "Cl"): ["NaCl", "Sodium Chloride", "Salt"],
    ("Cl", "Na"): ["NaCl", "Sodium Chloride", "Salt"],
    ("C", "O"): ["CO₂", "Carbon Dioxide", "(None)"],
    ("O", "C"): ["CO₂", "Carbon Dioxide", "(None)"],
    ("C", "O"): ["CO", "Carbon Monoxide", "(None)"],
    ("O", "C"): ["CO", "Carbon Monoxide", "(None)"],
    ("N", "H"): ["NH₃", "Nitrogen Trihydride", "Ammonia"],
    ("H", "N"): ["NH₃", "Nitrogen Trihydride", "Ammonia"],
    ("S", "O"): ["SO₂", "Sulfur Dioxide", "(None)"],
    ("O", "S"): ["SO₂", "Sulfur Dioxide", "(None)"],
    ("S", "O"): ["SO₃", "Sulfur Trioxide", "(None)"],
    ("O", "S"): ["SO₃", "Sulfur Trioxide", "(None)"],
    ("Mg", "O"): ["MgO", "Magnesium Oxide", "Magnesia"],
    ("O", "Mg"): ["MgO", "Magnesium Oxide", "Magnesia"],
    ("Al", "O"): ["Al₂O₃", "Aluminum Oxide", "Alumina"],
    ("O", "Al"): ["Al₂O₃", "Aluminum Oxide", "Alumina"],
    ("Fe", "O"): ["Fe₂O₃", "Iron(III) Oxide", "Rust"],
    ("O", "Fe"): ["Fe₂O₃", "Iron(III) Oxide", "Rust"],
    ("Fe", "O"): ["Fe₃O₄", "Iron(II,III) Oxide", "Magnetite"],
    ("O", "Fe"): ["Fe₃O₄", "Iron(II,III) Oxide", "Magnetite"],
    ("Cu", "O"): ["CuO", "Copper(II) Oxide", "(None)"],
    ("O", "Cu"): ["CuO", "Copper(II) Oxide", "(None)"],
    ("Cu", "O"): ["Cu₂O", "Copper(I) Oxide", "Cuprite"],
    ("O", "Cu"): ["Cu₂O", "Copper(I) Oxide", "Cuprite"],
    ("Zn", "O"): ["ZnO", "Zinc Oxide", "Zinc White"],
    ("O", "Zn"): ["ZnO", "Zinc Oxide", "Zinc White"],
    
    # Add more reactions as needed...
}

print("✅ Loaded 36 elements")
print("✅ Loaded reaction database")

# HTML frontend
HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VLABS - Virtual Chemistry Laboratory</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; padding: 20px;
        }
        .container {
            max-width: 1200px; margin: 0 auto; background: white;
            border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        header {
            background: linear-gradient(135deg, #2c3e50, #34495e);
            color: white; padding: 30px; text-align: center;
        }
        header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .lab-interface {
            display: grid; grid-template-columns: 1fr 1fr; gap: 30px;
            padding: 30px;
        }
        .control-panel, .reaction-area {
            background: #f8f9fa; padding: 25px;
            border-radius: 10px; border: 1px solid #e9ecef;
        }
        .elements-grid {
            display: grid; grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
            gap: 10px; margin-bottom: 20px; max-height: 400px; overflow-y: auto;
            padding: 10px; background: white; border-radius: 8px; border: 1px solid #ddd;
        }
        .element {
            background: linear-gradient(135deg, #74b9ff, #0984e3);
            color: white; padding: 15px 5px; border-radius: 8px;
            text-align: center; cursor: pointer; transition: all 0.3s ease;
            border: 2px solid transparent;
        }
        .element:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
        .element.selected { background: linear-gradient(135deg, #00b894, #00a085); border-color: #2ecc71; transform: scale(1.05); }
        .selected-list { display: flex; gap: 10px; margin: 15px 0; flex-wrap: wrap; }
        .selected-element {
            background: linear-gradient(135deg, #fdcb6e, #e17055);
            color: white; padding: 10px 15px; border-radius: 20px; font-weight: bold;
        }
        .react-button {
            background: linear-gradient(135deg, #e74c3c, #c0392b); color: white;
            border: none; padding: 15px 30px; font-size: 1.1em; border-radius: 25px;
            cursor: pointer; transition: all 0.3s ease; width: 100%; margin-top: 15px;
        }
        .react-button:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(231,76,60,0.4); }
        .react-button:disabled { background: #bdc3c7; cursor: not-allowed; }
        .output {
            background: white; padding: 20px; border-radius: 8px;
            min-height: 200px; border: 1px solid #ddd;
        }
        .reaction-success { animation: slideIn 0.5s ease; }
        @keyframes slideIn { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
        .reaction-equation { display: flex; align-items: center; justify-content: center; gap: 20px; font-size: 1.4em; margin: 20px 0; }
        .info-card { background: white; padding: 15px; border-radius: 8px; border: 2px solid #e9ecef; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔬 VLABS - Virtual Chemistry Laboratory</h1>
            <p>Experiment with chemical reactions! Select elements to see what compounds they form.</p>
            <div class="student-info">
                <strong>ADITYA BHARDWAJ</strong> | D2 | Roll No: 08 | B.TECH CSE
            </div>
        </header>

        <div class="lab-interface">
            <div class="control-panel">
                <h2>🧪 Periodic Table Elements</h2>
                <div class="elements-grid" id="elementsGrid"></div>

                <div class="selected-elements">
                    <h3>Selected Reactants:</h3>
                    <div id="selectedElements" class="selected-list">
                        <div class="empty-state">No elements selected</div>
                    </div>
                    <button id="reactBtn" class="react-button" disabled>⚡ Start Reaction</button>
                </div>
            </div>

            <div class="reaction-area">
                <h2>🔥 Reaction Results</h2>
                <div id="reactionOutput" class="output">
                    <div class="welcome-message">
                        <h3>Welcome to VLABS! 🧪</h3>
                        <p>Select 2 elements from the periodic table to discover chemical reactions.</p>
                        <div class="examples">
                            <strong>Try these combinations:</strong>
                            <div class="example-combinations">
                                <span class="example" onclick="setExample('H', 'O')">H + O = Water</span>
                                <span class="example" onclick="setExample('Na', 'Cl')">Na + Cl = Salt</span>
                                <span class="example" onclick="setExample('C', 'O')">C + O = CO₂</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const elementsGrid = document.getElementById("elementsGrid");
        const selectedElementsDiv = document.getElementById("selectedElements");
        const reactBtn = document.getElementById("reactBtn");
        const reactionOutput = document.getElementById("reactionOutput");

        let selectedElements = [];

        // Load elements
        fetch("/get_elements")
          .then(res => res.json())
          .then(elements => {
            elements.forEach(el => {
                const div = document.createElement("div");
                div.classList.add("element");
                div.innerHTML = `<div class="element-symbol">${el.symbol}</div><div class="element-name">${el.name}</div>`;
                div.addEventListener("click", () => toggleSelection(el.symbol, div));
                elementsGrid.appendChild(div);
            });
          });

        function toggleSelection(symbol, div) {
            if (selectedElements.includes(symbol)) {
                selectedElements = selectedElements.filter(el => el !== symbol);
                div.classList.remove("selected");
            } else if (selectedElements.length < 2) {
                selectedElements.push(symbol);
                div.classList.add("selected");
            }
            renderSelected();
            reactBtn.disabled = selectedElements.length !== 2;
        }

        function renderSelected() {
            selectedElementsDiv.innerHTML = "";
            selectedElements.forEach(el => {
                const span = document.createElement("div");
                span.classList.add("selected-element");
                span.innerText = el;
                selectedElementsDiv.appendChild(span);
            });
        }

        reactBtn.addEventListener("click", () => {
            if (selectedElements.length === 2) {
                const [el1, el2] = selectedElements;
                reactionOutput.innerHTML = '<div class="reaction-loading">🔍 Analyzing reaction...</div>';
                
                fetch(`/get_reaction?el1=${el1}&el2=${el2}`)
                  .then(res => res.json())
                  .then(data => {
                    if (data.type === "no_reaction") {
                        reactionOutput.innerHTML = `<div class="no-reaction"><h3>❌ No Reaction Found</h3><p>No reaction between ${data.reactants.join(" + ")}</p></div>`;
                    } else {
                        const [formula, iupac, common] = data.products;
                        reactionOutput.innerHTML = `
                            <div class="reaction-success">
                                <h3>✅ Reaction Successful!</h3>
                                <div class="reaction-equation">
                                    <div class="reactants">${data.reactants.join(" + ")}</div>
                                    <div class="arrow">→</div>
                                    <div class="products">${formula}</div>
                                </div>
                                <div class="info-card">
                                    <strong>Chemical Formula:</strong> ${formula}
                                </div>
                                <div class="info-card">
                                    <strong>IUPAC Name:</strong> ${iupac}
                                </div>
                                <div class="info-card">
                                    <strong>Common Name:</strong> ${common !== "(None)" ? common : "No common name"}
                                </div>
                            </div>
                        `;
                    }
                  });
            }
        });

        window.setExample = function(el1, el2) {
            // Clear current selection
            document.querySelectorAll('.element').forEach(el => el.classList.remove('selected'));
            selectedElements = [el1, el2];
            renderSelected();
            reactBtn.disabled = false;
            
            // Trigger reaction
            reactBtn.click();
        };
    </script>
</body>
</html>
'''

@app.route("/")
def home():
    return HTML

@app.route("/get_elements")
def get_elements():
    return jsonify(elements)

@app.route("/get_reaction")
def get_reaction():
    el1 = request.args.get("el1", "").strip()
    el2 = request.args.get("el2", "").strip()
    
    print(f"🧪 Reaction request: {el1} + {el2}")
    
    # Try both orders
    key1 = (el1, el2)
    key2 = (el2, el1)
    
    if key1 in reaction_map:
        print(f"✅ FOUND: {reaction_map[key1]}")
        return jsonify({
            "type": "binary", 
            "reactants": [el1, el2],
            "products": reaction_map[key1]
        })
    elif key2 in reaction_map:
        print(f"✅ FOUND: {reaction_map[key2]}")
        return jsonify({
            "type": "binary", 
            "reactants": [el1, el2],
            "products": reaction_map[key2]
        })
    
    print("❌ NOT FOUND")
    return jsonify({
        "type": "no_reaction",
        "reactants": [el1, el2],
        "products": ["No reaction found between these elements"]
    })

def open_browser():
    """Open the browser automatically after server starts"""
    time.sleep(2)
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    print("🚀 STARTING VLABS SERVER...")
    print("📡 Server will run on: http://127.0.0.1:5000")
    print("⏳ Starting server...")
    
    # Start browser in a separate thread
    threading.Thread(target=open_browser).start()
    
    # Start Flask server
    app.run(debug=True, port=5000, use_reloader=False)