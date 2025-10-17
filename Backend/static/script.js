// static/script.js
const elementsGrid = document.getElementById("elementsGrid");
const selectedElementsDiv = document.getElementById("selectedElements");
const reactBtn = document.getElementById("reactBtn");
const clearBtn = document.getElementById("clearBtn");
const reactionOutput = document.getElementById("reactionOutput");

let selectedElements = [];

// Load elements when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadElements();
});

function loadElements() {
    fetch("/get_elements")
        .then(res => res.json())
        .then(elements => {
            renderElements(elements);
        })
        .catch(error => {
            console.error('Error loading elements:', error);
            elementsGrid.innerHTML = '<div class="error">Error loading elements</div>';
        });
}

function renderElements(elements) {
    elementsGrid.innerHTML = "";
    
    elements.forEach(el => {
        const div = document.createElement("div");
        div.classList.add("element");
        div.innerHTML = `
            <div class="element-symbol">${el.symbol}</div>
            <div class="element-name">${el.name}</div>
        `;
        div.addEventListener("click", () => toggleSelection(el.symbol, div));
        elementsGrid.appendChild(div);
    });
}

function toggleSelection(symbol, div) {
    if (selectedElements.includes(symbol)) {
        // Deselect
        selectedElements = selectedElements.filter(el => el !== symbol);
        div.classList.remove("selected");
    } else if (selectedElements.length < 2) {
        // Select
        selectedElements.push(symbol);
        div.classList.add("selected");
    }
    renderSelected();
    updateReactButton();
}

function renderSelected() {
    selectedElementsDiv.innerHTML = "";
    
    if (selectedElements.length === 0) {
        selectedElementsDiv.innerHTML = '<div class="empty-state">No elements selected</div>';
        return;
    }
    
    selectedElements.forEach(el => {
        const span = document.createElement("div");
        span.classList.add("selected-element");
        span.innerHTML = `
            <span class="symbol">${el}</span>
            <span class="remove" onclick="removeElement('${el}')">×</span>
        `;
        selectedElementsDiv.appendChild(span);
    });
}

function removeElement(symbol) {
    selectedElements = selectedElements.filter(el => el !== symbol);
    const elementDiv = document.querySelector(`.element[data-symbol="${symbol}"]`);
    if (elementDiv) {
        elementDiv.classList.remove("selected");
    }
    renderSelected();
    updateReactButton();
}

function updateReactButton() {
    reactBtn.disabled = selectedElements.length !== 2;
    
    if (selectedElements.length === 2) {
        reactBtn.textContent = `⚡ React ${selectedElements.join(" + ")}`;
    } else {
        reactBtn.textContent = '⚡ Start Reaction';
    }
}

function performReaction() {
    if (selectedElements.length !== 2) return;

    const [el1, el2] = selectedElements;
    
    reactionOutput.innerHTML = `
        <div class="reaction-loading">
            <div class="loading-spinner"></div>
            <p>🔍 Analyzing reaction between ${el1} and ${el2}...</p>
        </div>
    `;
    
    fetch(`/get_reaction?el1=${el1}&el2=${el2}`)
        .then(res => res.json())
        .then(data => {
            displayReactionResults(data);
        })
        .catch(error => {
            console.error('Error:', error);
            reactionOutput.innerHTML = `
                <div class="error-message">
                    <h3> Error</h3>
                    <p>Failed to perform reaction. Make sure server is running.</p>
                </div>
            `;
        });
}

function displayReactionResults(data) {
    if (data.type === "no_reaction") {
        reactionOutput.innerHTML = `
            <div class="no-reaction">
                <h3> No Reaction Found</h3>
                <p>The elements <strong>${data.reactants.join(" + ")}</strong> do not form a known compound.</p>
            </div>
        `;
        return;
    }
    
    const [formula, iupac, common] = data.products;
    
    reactionOutput.innerHTML = `
        <div class="reaction-success">
            <div class="reaction-header">
                <h3> Reaction Successful!</h3>
            </div>
            <div class="reaction-equation">
                <div class="reactants">${data.reactants.join(" + ")}</div>
                <div class="arrow">→</div>
                <div class="products">${formula}</div>
            </div>
            <div class="reaction-info">
                <div class="info-card">
                    <h4>🧪 Chemical Formula</h4>
                    <div class="formula">${formula}</div>
                </div>
                <div class="info-card">
                    <h4> IUPAC Name</h4>
                    <div class="iupac-name">${iupac}</div>
                </div>
                <div class="info-card">
                    <h4> Common Name</h4>
                    <div class="common-name">${common !== "(None)" ? common : "No common name"}</div>
                </div>
            </div>
        </div>
    `;
}

// Clear all selection
clearBtn.addEventListener("click", function() {
    selectedElements.forEach(symbol => {
        const elementDiv = document.querySelector(`.element[data-symbol="${symbol}"]`);
        if (elementDiv) {
            elementDiv.classList.remove("selected");
        }
    });
    selectedElements = [];
    renderSelected();
    updateReactButton();
    reactionOutput.innerHTML = `
        <div class="welcome-message">
            <h3>Welcome to VLABS! </h3>
            <p>Select 2 elements from the periodic table to discover chemical reactions.</p>
        </div>
    `;
});

// React button event
reactBtn.addEventListener("click", performReaction);

// Example combinations
window.setExample = function(el1, el2) {
    // Clear current selection
    selectedElements.forEach(symbol => {
        const elementDiv = document.querySelector(`.element[data-symbol="${symbol}"]`);
        if (elementDiv) {
            elementDiv.classList.remove("selected");
        }
    });
    
    // Select new elements
    selectedElements = [el1, el2];
    selectedElements.forEach(symbol => {
        const elementDiv = document.querySelector(`.element[data-symbol="${symbol}"]`);
        if (elementDiv) {
            elementDiv.classList.add("selected");
        }
    });
    
    renderSelected();
    updateReactButton();
    performReaction();
};