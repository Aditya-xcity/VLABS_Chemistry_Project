#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <algorithm> 

// Helper function to trim whitespace from strings
std::string trim(const std::string& str) {
    const std::string WHITESPACE = " \t\n\r";
    size_t first = str.find_first_not_of(WHITESPACE);
    if (std::string::npos == first) {
        return str;
    }
    size_t last = str.find_last_not_of(WHITESPACE);
    return str.substr(first, (last - first + 1));
}

struct Reaction {
    std::string el1, el2, product_formula, product_name;
    int qty1, qty2;
};

int main() {
    std::ifstream db_file("database/reactions.csv");
    std::ifstream input_file("ipc/input.txt");
    std::ofstream output_file("ipc/output.txt");

    if (!db_file.is_open()) {
        output_file << "Error: Backend could not open database/reactions.csv";
        return 1;
    }
    if (!input_file.is_open()) {
        output_file << "Error: Backend could not open ipc/input.txt";
        return 1;
    }

    std::vector<Reaction> reactions;
    std::string line;

    while (getline(db_file, line)) {
        if (line.empty() || line[0] == '#') continue;

        std::stringstream ss(line);
        std::string part;
        Reaction r;
        
        getline(ss, r.el1, ',');             r.el1 = trim(r.el1);
        getline(ss, part, ',');              r.qty1 = std::stoi(trim(part));
        getline(ss, r.el2, ',');             r.el2 = trim(r.el2);
        getline(ss, part, ',');              r.qty2 = std::stoi(trim(part));
        getline(ss, r.product_formula, ','); r.product_formula = trim(r.product_formula);
        getline(ss, r.product_name);         r.product_name = trim(r.product_name);
        
        reactions.push_back(r);
    }
    db_file.close();
    
    std::string input_el1, input_el2;
    int input_qty1, input_qty2;
    input_file >> input_el1 >> input_qty1 >> input_el2 >> input_qty2;
    input_file.close();

    input_el1 = trim(input_el1);
    input_el2 = trim(input_el2);

    std::string result = "No reaction found for this combination.";
    for (const auto& r : reactions) {
        bool match1 = (r.el1 == input_el1 && r.qty1 == input_qty1 && r.el2 == input_el2 && r.qty2 == input_qty2);
        bool match2 = (r.el1 == input_el2 && r.qty1 == input_qty2 && r.el2 == input_el1 && r.qty2 == input_qty1);

        if (match1 || match2) {
            // THIS IS THE ONLY LINE THAT CHANGED
            result = "Product: " + r.product_formula + " (" + r.product_name + ")";
            break;
        }
    }
    
    output_file << result;
    output_file.close();

    return 0;
}