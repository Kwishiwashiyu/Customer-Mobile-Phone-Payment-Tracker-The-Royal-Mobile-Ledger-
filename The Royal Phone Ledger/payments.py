from db import get_connection
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import calendar

def record_payment(installment_id, amount):
    # ... (Existing logic for recording payment and updating status) ...
    conn = get_connection()
    if not conn: return False, "Connection Failed"
        
    cursor = conn.cursor()
    
    try:
        # 1. Update Balance
        cursor.execute("UPDATE installment_plans SET remaining_balance = remaining_balance - %s WHERE installment_id = %s", (amount, installment_id))
        
        # 2. Log Payment
        cursor.execute("INSERT INTO payments (installment_id, payment_date, amount) VALUES (%s, %s, %s)", (installment_id, date.today(), amount))
        
        # 3. Check Completion
        cursor.execute("SELECT remaining_balance FROM installment_plans WHERE installment_id = %s", (installment_id,))
        res = cursor.fetchone()
        msg = "Tribute Recorded."
        
        if res and res[0] <= 0:
            cursor.execute("UPDATE installment_plans SET status = 'Completed', remaining_balance = 0 WHERE installment_id = %s", (installment_id,))
            msg = "Tribute Recorded. The debt is fully paid! Rejoice!"

        conn.commit()
        conn.close()
        return True, msg
    except Exception as e:
        conn.close()
        return False, f"Database error: {e}"

def get_total_collected():
    # ... (Existing logic) ...
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(amount) FROM payments")
        res = cursor.fetchone()[0]
        conn.close()
        return res if res else 0.0
    return 0.0

# --- NEW FUNCTION: Get Payment History for a Loan ---
def get_payment_history(installment_id):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        sql = "SELECT payment_id, payment_date, amount, remarks FROM payments WHERE installment_id = %s ORDER BY payment_date DESC"
        cursor.execute(sql, (installment_id,))
        rows = cursor.fetchall()
        conn.close()
        return rows
    return []

# Check for Overdue Loans 
def get_overdue_loans():
    conn = get_connection()
    if not conn: 
        return [] # Ensures a list is returned if connection fails initially.
    
    overdue_list = []
    
    try:
        cursor = conn.cursor()
        today = date.today()

        # 1. Get all active loans and their details
        sql = """
        SELECT i.installment_id, c.last_name, i.purchase_date, i.months, i.monthly_payment
        FROM installment_plans i
        JOIN customers c ON i.customer_id = c.customer_id
        WHERE i.status = 'Active'
        """
        cursor.execute(sql)
        active_loans = cursor.fetchall()
        
        # 2. Iterate and check for overdue status (Relativedelta logic)
        from dateutil.relativedelta import relativedelta # Re-import here for clarity/safety
        
        for iid, last_name, purchase_date, total_months, monthly_payment in active_loans:
            delta = relativedelta(today, purchase_date)
            months_passed = (delta.years * 12) + delta.months
            expected_payments = min(max(1, months_passed), total_months)

            # Get the count and amount of payments actually made for this loan
            cursor.execute("SELECT COUNT(payment_id), SUM(amount) FROM payments WHERE installment_id = %s", (iid,))
            payment_info = cursor.fetchone()
            
            total_paid_amount = payment_info[1] if payment_info[1] else 0.0
            expected_amount = expected_payments * monthly_payment

            # Check if overdue
            if total_paid_amount < expected_amount:
                # Calculate the number of missed monthly payments (approximate)
                missed_count = expected_payments - (payment_info[0] if payment_info[0] else 0)
                
                overdue_list.append({
                    'id': iid,
                    'customer': last_name,
                    'monthly_due': f"{monthly_payment:.2f}",
                    'missed_payments': missed_count,
                    'status_flag': "⚠️ OVERDUE"
                })

        return overdue_list

    except Exception as e:
        # Catch any error during SQL execution (e.g., table missing)
        # We can optionally show the error, but we must return a list.
        # messagebox.showerror("Database Query Error", f"Failed to check overdue loans: {e}")
        return [] # Crucially returns an empty list on any error

    finally:
        if conn and conn.is_connected():
            conn.close()