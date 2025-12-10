import tkinter as tk
from tkinter import ttk
from payments import get_total_collected, get_overdue_loans
from db import get_connection

class DashboardGUI(tk.Frame):
    def __init__(self, parent, theme):
        super().__init__(parent, bg=theme['bg'])
        self.theme = theme
        
        tk.Button(self, text="🔄 Refresh Kingdom Stats", command=self.refresh,
                  bg=theme['accent'], fg="white", font=theme['font_btn']).pack(pady=10)
        
        # Main Stats Frame
        self.stats_frame = tk.Frame(self, bg=theme['bg'])
        self.stats_frame.pack(pady=20)
        
        # Overdue Report Frame
        report_label = tk.Label(self, text="⚠️ OVERDUE TRIBUTE REPORT ⚠️", font=theme['font_header'], 
                                bg=theme['bg'], fg="red")
        report_label.pack(pady=10)
        
        self.overdue_tree = self.create_overdue_table()
        self.overdue_tree.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.refresh()

    def create_overdue_table(self):
        cols = ("ID", "Subject", "Monthly Due", "Missed Payments", "Status")
        tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols: tree.heading(c, text=c)
        tree.column("ID", width=50, anchor='center')
        tree.column("Monthly Due", width=100, anchor='e')
        tree.column("Missed Payments", width=100, anchor='center')
        return tree

    def refresh(self):
        # 1. Update Main Stats
        for w in self.stats_frame.winfo_children(): w.destroy()
        
        conn = get_connection()
        if not conn: return
        cursor = conn.cursor()
        
        queries = {
            "Total Subjects": "SELECT COUNT(*) FROM customers",
            "Active Decrees": "SELECT COUNT(*) FROM installment_plans WHERE status='Active'",
            "Completed Decrees": "SELECT COUNT(*) FROM installment_plans WHERE status='Completed'"
        }
        
        row = 0
        for title, sql in queries.items():
            cursor.execute(sql)
            res = cursor.fetchone()[0]
            tk.Label(self.stats_frame, text=f"{title}: {res}", font=self.theme['font_header'], 
                     bg=self.theme['bg'], fg=self.theme['text']).grid(row=row, column=0, padx=20, pady=10)
            row += 1
            
        gold = get_total_collected()
        tk.Label(self.stats_frame, text=f"Total Gold Collected: {gold:.2f}", font=self.theme['font_header'], 
                 bg=self.theme['bg'], fg=self.theme['text']).grid(row=row, column=0, padx=20, pady=10)
        conn.close()

        # 2. Update Overdue Report
        for i in self.overdue_tree.get_children(): self.overdue_tree.delete(i)
        
        overdue_data = get_overdue_loans()
        for loan in overdue_data:
            self.overdue_tree.insert("", "end", values=(
                loan['id'], 
                loan['customer'], 
                loan['monthly_due'], 
                loan['missed_payments'], 
                loan['status_flag']
            ))