import tkinter as tk
from tkinter import ttk, messagebox
import installments

class InstallmentsGUI(tk.Frame):
    def __init__(self, parent, theme):
        super().__init__(parent, bg=theme['bg'])
        self.theme = theme
        self.build_ui()

    def build_ui(self):
        # Input Frame (Draft New Decree)
        frame = tk.LabelFrame(self, text="Draft New Decree", bg=self.theme['bg'], fg=self.theme['text'])
        frame.pack(fill="x", padx=10, pady=10)

        # Entries and Button for creation 
        self.cid = tk.Entry(frame, width=5)
        self.pid = tk.Entry(frame, width=5)
        self.months = tk.Entry(frame, width=5)
        self.rate = tk.Entry(frame, width=5)
        
        # Grid layout for inputs (recreated for context)
        tk.Label(frame, text="Cust ID:", bg=self.theme['bg']).grid(row=0, column=0); self.cid.grid(row=0, column=1)
        tk.Label(frame, text="Phone ID:", bg=self.theme['bg']).grid(row=0, column=2); self.pid.grid(row=0, column=3)
        tk.Label(frame, text="Months:", bg=self.theme['bg']).grid(row=0, column=4); self.months.grid(row=0, column=5)
        tk.Label(frame, text="Rate %:", bg=self.theme['bg']).grid(row=0, column=6); self.rate.grid(row=0, column=7)

        tk.Button(frame, text="Seal Decree", command=self.create_loan, bg=self.theme['accent'], fg="white").grid(row=0, column=8, padx=10)

        # Management Frame (Search, Close, Delete)
        manage_frame = tk.Frame(self, bg=self.theme['bg'])
        manage_frame.pack(fill="x", padx=10, pady=5)
        
        # Search Components
        tk.Label(manage_frame, text="Search Decree:", bg=self.theme['bg']).pack(side="left", padx=5)
        self.search_entry = tk.Entry(manage_frame, width=20)
        self.search_entry.pack(side="left", padx=5)
        tk.Button(manage_frame, text="Find", command=self.search_loans, bg=self.theme['accent'], fg="white").pack(side="left", padx=5)
        tk.Button(manage_frame, text="Reset View", command=self.load_data, bg=self.theme['highlight'], fg="white").pack(side="left", padx=5)
        
        # Action Buttons (Right side)
        tk.Button(manage_frame, text="Close Decree", command=self.close_loan, bg="#008080", fg="white").pack(side="right", padx=5)
        tk.Button(manage_frame, text="Delete Decree", command=self.delete_loan, bg="red", fg="white").pack(side="right", padx=5)


        # Loan Table
        cols = ("ID", "Customer", "Phone", "Total", "Monthly", "Balance", "Status")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols: self.tree.heading(c, text=c)
        self.tree.column("ID", width=50, anchor='center')
        self.tree.column("Total", width=100, anchor='e')
        self.tree.column("Monthly", width=100, anchor='e')
        self.tree.column("Balance", width=100, anchor='e')
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.load_data()
    
    def create_loan(self):
        try:
            success, msg = installments.create_installment(
                self.cid.get(), self.pid.get(), int(self.months.get()), float(self.rate.get())
            )
            if success:
                messagebox.showinfo("Success", msg)
                self.load_data()
            else:
                messagebox.showerror("Error", msg)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
    def load_data(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for row in installments.get_all_installments():
            self.tree.insert("", "end", values=row)

    def search_loans(self):
        query = self.search_entry.get().strip()
        if not query:
            self.load_data()
            return
        
        for i in self.tree.get_children(): self.tree.delete(i)
        for row in installments.search_installments(query):
            self.tree.insert("", "end", values=row)

    def close_loan(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Select a decree from the list to close.")
            return

        iid = self.tree.item(selected_item, 'values')[0]

        if messagebox.askyesno("Confirm Closing Decree", f"Are you sure you want to manually close Decree ID {iid}? Only proceed if Remaining Balance is zero or less."):
            success, msg = installments.close_installment(iid)
            if success:
                messagebox.showinfo("Success", msg)
            else:
                messagebox.showerror("Error", msg)
            self.load_data()

    # Delete Loan Function
    def delete_loan(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Select a decree from the list to delete.")
            return

        # Extract the installment ID (the first column value)
        iid = self.tree.item(selected_item, 'values')[0]

        # Confirmation dialog before performing a destructive action
        if messagebox.askyesno("Confirm Deletion", f"WARNING: Are you absolutely sure you want to PERMANENTLY DELETE Decree ID {iid}? This action cannot be undone and will revert phone stock."):
            
            success, msg = installments.delete_installment(iid)
            
            if success:
                messagebox.showinfo("Success", msg)
                self.load_data() # Refresh the table view
            else:
                messagebox.showerror("Error", msg)