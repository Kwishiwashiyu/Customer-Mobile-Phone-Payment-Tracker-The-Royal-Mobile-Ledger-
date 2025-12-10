import tkinter as tk
from tkinter import ttk, messagebox
import payments
from db import get_connection

class PaymentsGUI(tk.Frame):
    def __init__(self, parent, theme):
        super().__init__(parent, bg=theme['bg'])
        self.theme = theme
        self.build_ui()
        
    def build_ui(self):
        # Top Frame for Payment Entry and Status
        top_frame = tk.Frame(self, bg=self.theme['bg'])
        top_frame.pack(fill="x", padx=10, pady=10)
        
        # Left side: Payment Entry
        entry_frame = tk.LabelFrame(top_frame, text="Accept Tribute", bg=self.theme['bg'], fg=self.theme['text'])
        entry_frame.pack(side="left", padx=5, fill="y")

        tk.Label(entry_frame, text="Installment ID:", bg=self.theme['bg']).grid(row=0, column=0, padx=5, pady=5)
        self.iid = tk.Entry(entry_frame); self.iid.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Button(entry_frame, text="Fetch Decree Status", command=self.fetch_loan_details, bg=self.theme['highlight'], fg="white").grid(row=0, column=2, padx=5, pady=5)

        tk.Label(entry_frame, text="Amount:", bg=self.theme['bg']).grid(row=1, column=0, padx=5, pady=5)
        self.amt = tk.Entry(entry_frame); self.amt.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(entry_frame, text="Record Tribute", command=self.pay, bg=self.theme['accent'], fg="white").grid(row=1, column=2, padx=5, pady=5)

        # Right side: Status Display
        self.info_frame = tk.LabelFrame(top_frame, text="Current Decree Status", bg=self.theme['bg'], fg=self.theme['text'])
        self.info_frame.pack(side="right", padx=5, fill="y", expand=True)
        
        self.lbl_balance = tk.Label(self.info_frame, text="Remaining Balance: N/A", bg=self.theme['bg'], font=self.theme['font_body'])
        self.lbl_balance.pack(anchor='w', padx=10, pady=2)
        self.lbl_monthly = tk.Label(self.info_frame, text="Monthly Due: N/A", bg=self.theme['bg'], font=self.theme['font_body'])
        self.lbl_monthly.pack(anchor='w', padx=10, pady=2)
        self.lbl_status = tk.Label(self.info_frame, text="Status: N/A", bg=self.theme['bg'], font=self.theme['font_body'])
        self.lbl_status.pack(anchor='w', padx=10, pady=2)
        
        # Payment History Frame
        history_frame = tk.LabelFrame(self, text="📜 Payment Scroll (History)", bg=self.theme['bg'], fg=self.theme['text'])
        history_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        cols = ("ID", "Date", "Amount", "Remarks")
        self.tree_history = ttk.Treeview(history_frame, columns=cols, show="headings")
        for c in cols: self.tree_history.heading(c, text=c)
        self.tree_history.pack(fill="both", expand=True, padx=5, pady=5)

    def fetch_loan_details(self):
        iid = self.iid.get()
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            sql = "SELECT remaining_balance, monthly_payment, status FROM installment_plans WHERE installment_id = %s"
            cursor.execute(sql, (iid,))
            result = cursor.fetchone()
            conn.close()
            
            # Update history view and status view
            self.load_history(iid)
            
            if result:
                balance, monthly, status = result
                self.lbl_balance.config(text=f"Remaining Balance: {balance:.2f} Gold")
                self.lbl_monthly.config(text=f"Monthly Due: {monthly:.2f} Gold")
                self.lbl_status.config(text=f"Status: {status}")
            else:
                self.lbl_balance.config(text="Remaining Balance: Decree not found.")
                self.lbl_monthly.config(text="Monthly Due: N/A")
                self.lbl_status.config(text="Status: N/A")

    def load_history(self, iid):
        for i in self.tree_history.get_children(): self.tree_history.delete(i)
        
        history = payments.get_payment_history(iid)
        for row in history:
            self.tree_history.insert("", "end", values=row)

    def pay(self):
        try:
            iid = self.iid.get()
            amount = float(self.amt.get())
            success, msg = payments.record_payment(iid, amount)
            
            if success:
                messagebox.showinfo("Success", msg)
                self.amt.delete(0, 'end')
                self.fetch_loan_details() # Refresh status and history
            else:
                messagebox.showerror("Error", msg)
        except ValueError:
            messagebox.showerror("Error", "Invalid Amount")