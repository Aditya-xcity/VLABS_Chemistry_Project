import tkinter as tk
from tkinter import ttk, font
import subprocess
import os
import sys
import time

# --- Smart Path Configuration ---
try:
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
except NameError:
    PROJECT_ROOT = os.path.abspath('.')

IPC_DIR = os.path.join(PROJECT_ROOT, 'ipc')
DATABASE_DIR = os.path.join(PROJECT_ROOT, 'database')
BACKEND_EXE_PATH = os.path.join(PROJECT_ROOT, 'backend', 'main.exe')
INPUT_FILE_PATH = os.path.join(IPC_DIR, 'input.txt')
OUTPUT_FILE_PATH = os.path.join(IPC_DIR, 'output.txt')

# --- Periodic Table Data and Colors ---
PERIODIC_TABLE_LAYOUT = [
    ('H', 0, 0), ('He', 0, 17),
    ('Li', 1, 0), ('Be', 1, 1), ('B', 1, 12), ('C', 1, 13), ('N', 1, 14), ('O', 1, 15), ('F', 1, 16), ('Ne', 1, 17),
    ('Na', 2, 0), ('Mg', 2, 1), ('Al', 2, 12), ('Si', 2, 13), ('P', 2, 14), ('S', 2, 15), ('Cl', 2, 16), ('Ar', 2, 17),
    ('K', 3, 0), ('Ca', 3, 1), ('Sc', 3, 2), ('Ti', 3, 3), ('V', 3, 4), ('Cr', 3, 5), ('Mn', 3, 6), ('Fe', 3, 7), ('Co', 3, 8), ('Ni', 3, 9), ('Cu', 3, 10), ('Zn', 3, 11), ('Ga', 3, 12), ('Ge', 3, 13), ('As', 3, 14), ('Se', 3, 15), ('Br', 3, 16), ('Kr', 3, 17),
    ('Rb', 4, 0), ('Sr', 4, 1), ('Y', 4, 2), ('Zr', 4, 3), ('Nb', 4, 4), ('Mo', 4, 5), ('Tc', 4, 6), ('Ru', 4, 7), ('Rh', 4, 8), ('Pd', 4, 9), ('Ag', 4, 10), ('Cd', 4, 11), ('In', 4, 12), ('Sn', 4, 13), ('Sb', 4, 14), ('Te', 4, 15), ('I', 4, 16), ('Xe', 4, 17),
    ('Cs', 5, 0), ('Ba', 5, 1), ('La', 5, 2), ('Hf', 5, 3), ('Ta', 5, 4), ('W', 5, 5), ('Re', 5, 6), ('Os', 5, 7), ('Ir', 5, 8), ('Pt', 5, 9), ('Au', 5, 10), ('Hg', 5, 11), ('Tl', 5, 12), ('Pb', 5, 13), ('Bi', 5, 14), ('Po', 5, 15), ('At', 5, 16), ('Rn', 5, 17),
    ('Fr', 6, 0), ('Ra', 6, 1), ('Ac', 6, 2), ('Rf', 6, 3), ('Db', 6, 4), ('Sg', 6, 5), ('Bh', 6, 6), ('Hs', 6, 7), ('Mt', 6, 8), ('Ds', 6, 9), ('Rg', 6, 10), ('Cn', 6, 11), ('Nh', 6, 12), ('Fl', 6, 13), ('Mc', 6, 14), ('Lv', 6, 15), ('Ts', 6, 16), ('Og', 6, 17),
    ('Ce', 8, 3), ('Pr', 8, 4), ('Nd', 8, 5), ('Pm', 8, 6), ('Sm', 8, 7), ('Eu', 8, 8), ('Gd', 8, 9), ('Tb', 8, 10), ('Dy', 8, 11), ('Ho', 8, 12), ('Er', 8, 13), ('Tm', 8, 14), ('Yb', 8, 15), ('Lu', 8, 16),
    ('Th', 9, 3), ('Pa', 9, 4), ('U', 9, 5), ('Np', 9, 6), ('Pu', 9, 7), ('Am', 9, 8), ('Cm', 9, 9), ('Bk', 9, 10), ('Cf', 9, 11), ('Es', 9, 12), ('Fm', 9, 13), ('Md', 9, 14), ('No', 9, 15), ('Lr', 9, 16)
]
ELEMENT_TYPES = {
    'H': 'Nonmetal', 'He': 'Noble Gas', 'Li': 'Alkali Metal', 'Be': 'Alkaline Earth Metal', 'B': 'Metalloid', 'C': 'Nonmetal', 'N': 'Nonmetal', 'O': 'Nonmetal', 'F': 'Nonmetal', 'Ne': 'Noble Gas',
    'Na': 'Alkali Metal', 'Mg': 'Alkaline Earth Metal', 'Al': 'Post-transition Metal', 'Si': 'Metalloid', 'P': 'Nonmetal', 'S': 'Nonmetal', 'Cl': 'Nonmetal', 'Ar': 'Noble Gas',
    'K': 'Alkali Metal', 'Ca': 'Alkaline Earth Metal', 'Sc': 'Transition Metal', 'Ti': 'Transition Metal', 'V': 'Transition Metal', 'Cr': 'Transition Metal', 'Mn': 'Transition Metal', 'Fe': 'Transition Metal', 'Co': 'Transition Metal', 'Ni': 'Transition Metal', 'Cu': 'Transition Metal', 'Zn': 'Transition Metal', 'Ga': 'Post-transition Metal', 'Ge': 'Metalloid', 'As': 'Metalloid', 'Se': 'Nonmetal', 'Br': 'Nonmetal', 'Kr': 'Noble Gas',
    'Rb': 'Alkali Metal', 'Sr': 'Alkaline Earth Metal', 'Y': 'Transition Metal', 'Zr': 'Transition Metal', 'Nb': 'Transition Metal', 'Mo': 'Transition Metal', 'Tc': 'Transition Metal', 'Ru': 'Transition Metal', 'Rh': 'Transition Metal', 'Pd': 'Transition Metal', 'Ag': 'Transition Metal', 'Cd': 'Post-transition Metal', 'In': 'Post-transition Metal', 'Sn': 'Post-transition Metal', 'Sb': 'Metalloid', 'Te': 'Metalloid', 'I': 'Nonmetal', 'Xe': 'Noble Gas',
    'Cs': 'Alkali Metal', 'Ba': 'Alkaline Earth Metal', 'La': 'Lanthanide', 'Hf': 'Transition Metal', 'Ta': 'Transition Metal', 'W': 'Transition Metal', 'Re': 'Transition Metal', 'Os': 'Transition Metal', 'Ir': 'Transition Metal', 'Pt': 'Transition Metal', 'Au': 'Transition Metal', 'Hg': 'Post-transition Metal', 'Tl': 'Post-transition Metal', 'Pb': 'Post-transition Metal', 'Bi': 'Post-transition Metal', 'Po': 'Metalloid', 'At': 'Metalloid', 'Rn': 'Noble Gas',
    'Fr': 'Alkali Metal', 'Ra': 'Alkaline Earth Metal', 'Ac': 'Actinide', 'Rf': 'Transition Metal', 'Db': 'Transition Metal', 'Sg': 'Transition Metal', 'Bh': 'Transition Metal', 'Hs': 'Transition Metal', 'Mt': 'Transition Metal', 'Ds': 'Transition Metal', 'Rg': 'Transition Metal', 'Cn': 'Transition Metal', 'Nh': 'Post-transition Metal', 'Fl': 'Post-transition Metal', 'Mc': 'Post-transition Metal', 'Lv': 'Post-transition Metal', 'Ts': 'Post-transition Metal', 'Og': 'Unknown Property',
    'Ce': 'Lanthanide', 'Pr': 'Lanthanide', 'Nd': 'Lanthanide', 'Pm': 'Lanthanide', 'Sm': 'Lanthanide', 'Eu': 'Lanthanide', 'Gd': 'Lanthanide', 'Tb': 'Lanthanide', 'Dy': 'Lanthanide', 'Ho': 'Lanthanide', 'Er': 'Lanthanide', 'Tm': 'Lanthanide', 'Yb': 'Lanthanide', 'Lu': 'Lanthanide',
    'Th': 'Actinide', 'Pa': 'Actinide', 'U': 'Actinide', 'Np': 'Actinide', 'Pu': 'Actinide', 'Am': 'Actinide', 'Cm': 'Actinide', 'Bk': 'Actinide', 'Cf': 'Actinide', 'Es': 'Actinide', 'Fm': 'Actinide', 'Md': 'Actinide', 'No': 'Actinide', 'Lr': 'Actinide'
}
TYPE_COLORS = {
    'Alkali Metal': '#FF6666', 'Alkaline Earth Metal': '#FFD700', 'Transition Metal': '#ADD8E6',
    'Post-transition Metal': '#90EE90', 'Metalloid': '#FFC0CB', 'Nonmetal': '#FFA07A',
    'Noble Gas': '#BA55D3', 'Lanthanide': '#FFE4B5', 'Actinide': '#E6E6FA', 'Unknown Property': '#D3D3D3'
}

class ChemLabApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("VLabs Chemistry")
        self.geometry("850x820")

        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.configure(bg="#e0e0e0")

        self.style.configure('TFrame', background='#e0e0e0')
        self.style.configure('TLabel', background='#e0e0e0', font=('Segoe UI', 10))
        self.style.configure('TLabelframe', background='#e0e0e0', borderwidth=1, relief="groove")
        self.style.configure('TLabelframe.Label', background='#e0e0e0', font=('Segoe UI', 11, 'bold'))
        
        for el_type, color in TYPE_COLORS.items():
            self.style.configure(f'{el_type}.TButton', 
                                 font=('Segoe UI', 9, 'bold'), 
                                 padding=5, 
                                 background=color,
                                 foreground='#333333' if el_type not in ['Noble Gas', 'Actinide'] else '#000000')
            self.style.map(f'{el_type}.TButton',
                background=[('active', '#c0e0f0'), ('!active', color)],
                relief=[('pressed', 'sunken'), ('!pressed', 'raised')])

        self.style.configure('React.TButton', font=('Segoe UI', 12, 'bold'), foreground='white', background='#2a75bb')
        self.style.map('React.TButton', background=[('active', '#3c8cd8')])
        
        self.style.configure('QtyArrow.TButton', font=('Segoe UI', 6), padding=(1,0))
        self.style.configure('Highlight.TLabel', background='#cce7ff', foreground="#333", anchor="center")
        self.style.configure('Normal.TLabel', background='#ffffff', foreground="#333", anchor="center")

        self.el1_var = tk.StringVar(value="?")
        self.el2_var = tk.StringVar(value="?")
        self.active_selector_id = 1

        main_frame = ttk.Frame(self, padding="15")
        main_frame.pack(fill="both", expand=True)

        top_labelframe = ttk.LabelFrame(main_frame, text="Reaction Chamber")
        top_labelframe.pack(fill="x", pady=(0, 10), ipady=10, ipadx=5)
        self.create_top_panel(top_labelframe)

        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill="x", pady=(5, 15))
        react_button = ttk.Button(bottom_frame, text="⚡ Perform Reaction", style='React.TButton', command=self.perform_reaction)
        react_button.pack(ipady=8)

        table_frame = ttk.LabelFrame(main_frame, text="Click a Slot, then Click an Element")
        table_frame.pack(fill="both", expand=True)
        self.create_periodic_table(table_frame)
        
        legend_labelframe = ttk.LabelFrame(main_frame, text="Legend")
        legend_labelframe.pack(fill="x", pady=5, ipady=5)
        self.create_legend(legend_labelframe)

        self.set_active_selector(1)

    def create_top_panel(self, parent):
        parent.columnconfigure((0, 2, 4), weight=1)

        controller1_frame = ttk.Frame(parent)
        controller1_frame.grid(row=0, column=0, rowspan=2)
        self.slot1_frame, self.qty1_entry = self.create_element_controller(controller1_frame, self.el1_var, 1)
        self.slot1_frame.winfo_children()[0].bind("<Button-1>", lambda e: self.set_active_selector(1))
        self.qty1_entry.insert(0, "1")

        plus_label = ttk.Label(parent, text="+", font=('Segoe UI', 28, 'bold'))
        plus_label.grid(row=0, column=1, rowspan=2, sticky='nsew', padx=10)

        controller2_frame = ttk.Frame(parent)
        controller2_frame.grid(row=0, column=2, rowspan=2)
        self.slot2_frame, self.qty2_entry = self.create_element_controller(controller2_frame, self.el2_var, 2)
        self.slot2_frame.winfo_children()[0].bind("<Button-1>", lambda e: self.set_active_selector(2))
        self.qty2_entry.insert(0, "1")
        
        arrow_label = ttk.Label(parent, text="→", font=('Segoe UI', 28, 'bold'))
        arrow_label.grid(row=0, column=3, rowspan=2, sticky='nsew', padx=10)
        
        self.result_label = ttk.Label(
            parent, text="Result Appears Here", font=('Segoe UI', 12, 'italic'), 
            anchor='center', padding=10, relief='groove', background='#ffffff',
            wraplength=200, justify='center'
        )
        self.result_label.grid(row=0, column=4, rowspan=2, sticky='nsew')
    
    def create_element_controller(self, parent, var, selector_id):
        parent.columnconfigure(0, weight=1)

        slot_frame = ttk.Frame(parent, relief='sunken', cursor="hand2", width=160, height=70)
        slot_frame.grid(row=0, column=0, sticky='ew')
        slot_frame.grid_propagate(False)
        slot_frame.columnconfigure(0, weight=1)
        # --- THIS IS THE ONLY LINE THAT HAS BEEN ADDED ---
        slot_frame.rowconfigure(0, weight=1)

        slot_label = ttk.Label(slot_frame, textvariable=var, font=('Segoe UI', 32, 'bold'), style='Normal.TLabel')
        slot_label.grid(row=0, column=0, sticky="nsew")

        qty_frame = ttk.Frame(parent)
        qty_frame.grid(row=1, column=0, pady=5)
        
        ttk.Label(qty_frame, text="Atoms:").pack(side='left', padx=(0, 5))
        
        entry = ttk.Entry(qty_frame, width=4, font=('Segoe UI', 10), justify='center')
        entry.pack(side='left')

        button_frame = ttk.Frame(qty_frame)
        button_frame.pack(side='left', fill='y')

        up_button = ttk.Button(button_frame, text="▲", style='QtyArrow.TButton', command=lambda e=entry: self.increase_qty(e))
        up_button.pack(padx=(2,0))

        down_button = ttk.Button(button_frame, text="▼", style='QtyArrow.TButton', command=lambda e=entry: self.decrease_qty(e))
        down_button.pack(padx=(2,0))

        return slot_frame, entry

    def increase_qty(self, entry_widget):
        try:
            current_value = int(entry_widget.get())
            entry_widget.delete(0, 'end')
            entry_widget.insert(0, str(current_value + 1))
        except ValueError:
            entry_widget.delete(0, 'end')
            entry_widget.insert(0, "1")

    def decrease_qty(self, entry_widget):
        try:
            current_value = int(entry_widget.get())
            if current_value > 1:
                entry_widget.delete(0, 'end')
                entry_widget.insert(0, str(current_value - 1))
        except ValueError:
            entry_widget.delete(0, 'end')
            entry_widget.insert(0, "1")
    
    def set_active_selector(self, selector_id):
        self.active_selector_id = selector_id
        
        label1 = self.slot1_frame.winfo_children()[0]
        label2 = self.slot2_frame.winfo_children()[0]
        
        if selector_id == 1:
            label1.config(style='Highlight.TLabel')
            label2.config(style='Normal.TLabel')
        else:
            label1.config(style='Normal.TLabel')
            label2.config(style='Highlight.TLabel')

    def create_periodic_table(self, parent):
        ttk.Label(parent, text="").grid(row=7, column=0)
        
        for symbol, row, col in PERIODIC_TABLE_LAYOUT:
            element_type = ELEMENT_TYPES.get(symbol, 'Unknown Property')
            button = ttk.Button(parent, text=symbol, style=f'{element_type}.TButton', width=3,
                                command=lambda s=symbol: self.on_element_click(s))
            button.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
        
        for i in range(18): parent.columnconfigure(i, weight=1)
        for i in range(10): parent.rowconfigure(i, weight=1)

    def on_element_click(self, symbol):
        if self.active_selector_id == 1:
            self.el1_var.set(symbol)
            self.set_active_selector(2)
        else:
            self.el2_var.set(symbol)
            self.set_active_selector(1)

    def create_legend(self, parent):
        parent.columnconfigure(tuple(range(10)), weight=1)
        
        col_num = 0
        for el_type, color in TYPE_COLORS.items():
            frame = ttk.Frame(parent)
            frame.grid(row=0, column=col_num, padx=5, pady=2, sticky='w')
            
            color_box = tk.Canvas(frame, width=15, height=15, bg=color, relief="raised", bd=1)
            color_box.pack(side="left", padx=(0, 5))
            
            ttk.Label(frame, text=el_type, font=('Segoe UI', 8)).pack(side="left")
            col_num += 1

    def perform_reaction(self):
        el1 = self.el1_var.get()
        el2 = self.el2_var.get()

        if el1 == "?" or el2 == "?":
            self.result_label.config(text="Error: Please select two elements.")
            return

        qty1 = self.qty1_entry.get()
        qty2 = self.qty2_entry.get()

        if not qty1.isdigit() or not qty2.isdigit() or int(qty1) <= 0 or int(qty2) <= 0:
            self.result_label.config(text="Error: Enter valid, positive numbers.")
            return

        self.result_label.config(text="Calculating...")
        self.update()

        os.makedirs(IPC_DIR, exist_ok=True)
        with open(INPUT_FILE_PATH, "w", encoding="utf-8") as f:
            f.write(f"{el1} {qty1} {el2} {qty2}")

        if os.path.exists(OUTPUT_FILE_PATH):
            os.remove(OUTPUT_FILE_PATH)

        try:
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.run([BACKEND_EXE_PATH], check=True, startupinfo=si, cwd=PROJECT_ROOT)
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.result_label.config(text=f"Error: main.exe not found at {BACKEND_EXE_PATH}")
            return

        result = "Error: Backend produced no output."
        for _ in range(20):
            if os.path.exists(OUTPUT_FILE_PATH):
                time.sleep(0.05)
                with open(OUTPUT_FILE_PATH, "r", encoding="utf-8") as f:
                    result = f.read()
                break
            time.sleep(0.1)

        self.result_label.config(text=result)


if __name__ == "__main__":
    app = ChemLabApp()
    app.mainloop()