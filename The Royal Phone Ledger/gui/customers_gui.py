import tkinter as tk
from tkinter import ttk, messagebox
import customers

class CustomersGUI(tk.Frame):
    def __init__(self, parent, theme):
        super().__init__(parent, bg=theme['bg'])
        self.theme = theme
        self.selected_customer_id = None # State variable to track which customer is selected
        self.build_ui()

    def build_ui(self):
        # Form Frame
        form_frame = tk.LabelFrame(self, text="Subject Registry", bg=self.theme['bg'], fg=self.theme['text'])
        form_frame.pack(fill="x", padx=10, pady=10)

        self.entries = {}
        fields = ["First Name", "Last Name", "Contact"]
        for i, field in enumerate(fields):
            tk.Label(form_frame, text=field+":", bg=self.theme['bg']).grid(row=0, column=i*2, padx=5, pady=5)
            e = tk.Entry(form_frame)
            e.grid(row=0, column=i*2+1, padx=5, pady=5)
            self.entries[field] = e
        
        # Button Frame
        btn_frame = tk.Frame(form_frame, bg=self.theme['bg'])
        btn_frame.grid(row=0, column=6, padx=10)

        tk.Button(btn_frame, text="Add Subject", command=self.add_customer, bg=self.theme['accent'], fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Update Subject", command=self.update_customer, bg=self.theme['highlight'], fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Ban Subject (Delete)", command=self.delete_customer, bg="red", fg="white").pack(side="left", padx=5)
        
        # Table
        cols = ("ID", "First Name", "Last Name", "Contact")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols: self.tree.heading(c, text=c)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tree.bind('<<TreeviewSelect>>', self.select_customer)
        self.load_data()

    def select_customer(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            values = self.tree.item(selected_item, 'values')
            self.selected_customer_id = values[0]
            
            # Clear and populate entries
            for e in self.entries.values(): e.delete(0, 'end')
            self.entries["First Name"].insert(0, values[1])
            self.entries["Last Name"].insert(0, values[2])
            self.entries["Contact"].insert(0, values[3])
        else:
            self.selected_customer_id = None

    def add_customer(self):
        customers.add_customer(self.entries["First Name"].get(), self.entries["Last Name"].get(), self.entries["Contact"].get())
        self.load_data()
        messagebox.showinfo("Success", "Subject added to the Royal Registry!")
        for e in self.entries.values(): e.delete(0, 'end')

    def update_customer(self):
        if not self.selected_customer_id:
            messagebox.showerror("Error", "Select a subject from the list to update.")
            return

        customers.update_customer(self.selected_customer_id, 
                                  self.entries["First Name"].get(), 
                                  self.entries["Last Name"].get(), 
                                  self.entries["Contact"].get())
        
        messagebox.showinfo("Success", f"Subject ID {self.selected_customer_id} updated.")
        self.load_data()

    def delete_customer(self):
        if not self.selected_customer_id:
            messagebox.showerror("Error", "Select a subject from the list to delete.")
            return
            
        if messagebox.askyesno("Confirm Banishment", f"Are you sure you wish to banish Subject ID {self.selected_customer_id}?"):
            success, msg = customers.delete_customer(self.selected_customer_id)
            if success:
                messagebox.showinfo("Success", msg)
            else:
                messagebox.showerror("Error", msg)
            self.load_data()
            for e in self.entries.values(): e.delete(0, 'end')

    def load_data(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for row in customers.get_all_customers():
            self.tree.insert("", "end", values=row)