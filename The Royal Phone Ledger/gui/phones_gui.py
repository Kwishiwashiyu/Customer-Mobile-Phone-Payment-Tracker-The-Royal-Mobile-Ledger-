import tkinter as tk
from tkinter import ttk, messagebox
import phones

class PhonesGUI(tk.Frame):
    def __init__(self, parent, theme):
        super().__init__(parent, bg=theme['bg'])
        self.theme = theme
        self.selected_phone_id = None # State variable to track selected phone
        self.build_ui()

    def build_ui(self):
        frame = tk.LabelFrame(self, text="Forge New Weapon (Phone)", bg=self.theme['bg'], fg=self.theme['text'])
        frame.pack(fill="x", padx=10, pady=10)

        self.e_model = tk.Entry(frame); self.e_price = tk.Entry(frame); self.e_stock = tk.Entry(frame)
        
        tk.Label(frame, text="Model:", bg=self.theme['bg']).grid(row=0, column=0)
        self.e_model.grid(row=0, column=1, padx=5)
        tk.Label(frame, text="Price:", bg=self.theme['bg']).grid(row=0, column=2)
        self.e_price.grid(row=0, column=3, padx=5)
        tk.Label(frame, text="Stock:", bg=self.theme['bg']).grid(row=0, column=4)
        self.e_stock.grid(row=0, column=5, padx=5)
        
        # Button Frame
        btn_frame = tk.Frame(frame, bg=self.theme['bg'])
        btn_frame.grid(row=0, column=6, padx=10)

        tk.Button(btn_frame, text="Forge Item (Add)", command=self.add_phone, bg=self.theme['accent'], fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Reforge (Update)", command=self.update_phone, bg=self.theme['highlight'], fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Scrap (Delete)", command=self.delete_phone, bg="red", fg="white").pack(side="left", padx=5)

        cols = ("ID", "Model", "Price", "Stock")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols: self.tree.heading(c, text=c)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tree.bind('<<TreeviewSelect>>', self.select_phone)
        self.load_data()

    def select_phone(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            values = self.tree.item(selected_item, 'values')
            self.selected_phone_id = values[0]
            
            # Clear and populate entries
            self.e_model.delete(0,'end'); self.e_price.delete(0,'end'); self.e_stock.delete(0,'end')
            self.e_model.insert(0, values[1])
            self.e_price.insert(0, values[2])
            self.e_stock.insert(0, values[3])
        else:
            self.selected_phone_id = None

    def add_phone(self):
        phones.add_phone(self.e_model.get(), self.e_price.get(), self.e_stock.get())
        self.load_data()
        self.e_model.delete(0,'end'); self.e_price.delete(0,'end'); self.e_stock.delete(0,'end')

    def update_phone(self):
        if not self.selected_phone_id:
            messagebox.showerror("Error", "Select a weapon from the Armory to reforge.")
            return

        phones.update_phone(self.selected_phone_id, 
                            self.e_model.get(), 
                            self.e_price.get(), 
                            self.e_stock.get())
        
        messagebox.showinfo("Success", f"Weapon ID {self.selected_phone_id} updated.")
        self.load_data()

    def delete_phone(self):
        if not self.selected_phone_id:
            messagebox.showerror("Error", "Select a weapon from the Armory to scrap.")
            return
            
        if messagebox.askyesno("Confirm Scrap", f"Are you sure you wish to scrap Weapon ID {self.selected_phone_id}?"):
            success, msg = phones.delete_phone(self.selected_phone_id)
            if success:
                messagebox.showinfo("Success", msg)
            else:
                messagebox.showerror("Error", msg)
            self.load_data()
            self.e_model.delete(0,'end'); self.e_price.delete(0,'end'); self.e_stock.delete(0,'end')

    def load_data(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for row in phones.get_all_phones():
            self.tree.insert("", "end", values=row)