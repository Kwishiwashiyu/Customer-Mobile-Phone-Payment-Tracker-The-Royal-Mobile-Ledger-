import tkinter as tk
from tkinter import ttk

# Import GUI Modules
from gui.dashboard_gui import DashboardGUI
from gui.customers_gui import CustomersGUI
from gui.phones_gui import PhonesGUI
from gui.installments_gui import InstallmentsGUI
from gui.payments_gui import PaymentsGUI

# --- MEDIEVAL THEME CONSTANTS ---
THEME = {
    'bg': "#F5E6C4",        # Parchment
    'text': "#3E2723",      # Dark Ink
    'accent': "#5D4037",    # Leather
    'highlight': "#8D6E63", # Light Leather
    'font_header': ("Times New Roman", 20, "bold"),
    'font_body': ("Times New Roman", 12),
    'font_btn': ("Times New Roman", 12, "bold")
}

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("The Royal Phone Ledger")
        self.root.geometry("1000x700")
        self.root.configure(bg=THEME['bg'])
        
        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Notebook (Tabs)
        style.configure("TNotebook", background=THEME['bg'], borderwidth=0)
        style.configure("TNotebook.Tab", background=THEME['accent'], foreground="#FFFFFF", 
                        font=THEME['font_btn'], padding=[10, 5])
        style.map("TNotebook.Tab", background=[("selected", THEME['highlight'])])
        
        # Treeview (Tables)
        style.configure("Treeview", background="#FFF8E1", fieldbackground="#FFF8E1", 
                        foreground=THEME['text'], font=THEME['font_body'])
        style.configure("Treeview.Heading", background=THEME['accent'], foreground="#FFFFFF", 
                        font=THEME['font_btn'])

    def create_widgets(self):
        # Header
        header = tk.Frame(self.root, bg=THEME['bg'])
        header.pack(fill="x", pady=20)
        tk.Label(header, text="📜 The Royal Phone Ledger 📜", font=("Old English Text MT", 30), 
                 bg=THEME['bg'], fg=THEME['text']).pack()

        # Navigation
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill="both", padx=20, pady=10)

        # Tabs
        self.add_tab(notebook, DashboardGUI(notebook, THEME), "🏰 Kingdom Overview")
        self.add_tab(notebook, CustomersGUI(notebook, THEME), "👥 Subjects")
        self.add_tab(notebook, PhonesGUI(notebook, THEME), "⚔️ Armory")
        self.add_tab(notebook, InstallmentsGUI(notebook, THEME), "💰 Decrees")
        self.add_tab(notebook, PaymentsGUI(notebook, THEME), "⚖️ Tribute")

    def add_tab(self, notebook, frame, text):
        notebook.add(frame, text=text)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()