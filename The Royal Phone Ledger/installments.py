from db import get_connection
from datetime import date
from tkinter import messagebox

def create_installment(customer_id, phone_id, months, rate):
    conn = get_connection()
    if not conn: return False, "Connection Failed"
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT price, stock FROM phones WHERE phone_id = %s", (phone_id,))
        phone_data = cursor.fetchone()
        if not phone_data or phone_data[1] < 1:
            conn.close()
            return False, "Item out of stock or does not exist."

        price = float(phone_data[0])
        total_amount = price + (price * (rate / 100))
        monthly_payment = total_amount / months
        
        sql = """INSERT INTO installment_plans 
                  (customer_id, phone_id, purchase_date, months, interest_rate, 
                   total_amount, monthly_payment, remaining_balance, status) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Active')"""
        
        val = (customer_id, phone_id, date.today(), months, rate, total_amount, monthly_payment, total_amount)
        cursor.execute(sql, val)
        cursor.execute("UPDATE phones SET stock = stock - 1 WHERE phone_id = %s", (phone_id,))
        
        conn.commit()
        conn.close()
        return True, f"Decree Sealed! Monthly Tribute: {monthly_payment:.2f}"
    except Exception as e:
        conn.close()
        return False, str(e)

# Fetch All Installments Function
def get_all_installments():
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        sql = """SELECT i.installment_id, c.last_name, p.model_name, 
                 i.total_amount, i.monthly_payment, i.remaining_balance, i.status
                 FROM installment_plans i 
                 JOIN customers c ON i.customer_id = c.customer_id 
                 JOIN phones p ON i.phone_id = p.phone_id"""
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        return rows
    return []

# Close Installment Function
def close_installment(installment_id):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT remaining_balance FROM installment_plans WHERE installment_id = %s", (installment_id,))
            balance = cursor.fetchone()
            
            if balance is None:
                conn.close()
                return False, "Decree ID not found."
            
            if balance[0] > 0:
                conn.close()
                return False, f"Balance is still {balance[0]:.2f}. Cannot close while debt remains."

            sql = "UPDATE installment_plans SET status = 'Completed' WHERE installment_id = %s"
            cursor.execute(sql, (installment_id,))
            conn.commit()
            conn.close()
            return True, f"Decree ID {installment_id} manually marked as Completed."
        except Exception as e:
            conn.close()
            return False, f"Error closing decree: {e}"
    return False, "Database connection failed."

def search_installments(query):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        search_term = f'%{query}%'
        # Search by ID or Customer Last Name or Phone Model
        sql = """SELECT i.installment_id, c.last_name, p.model_name, 
                 i.total_amount, i.monthly_payment, i.remaining_balance, i.status 
                 FROM installment_plans i 
                 JOIN customers c ON i.customer_id = c.customer_id 
                 JOIN phones p ON i.phone_id = p.phone_id
                 WHERE i.installment_id = %s OR c.last_name LIKE %s OR p.model_name LIKE %s"""
        cursor.execute(sql, (query, search_term, search_term))
        rows = cursor.fetchall()
        conn.close()
        return rows
    return []

# Delete Loan/Decree Function
def delete_installment(installment_id):
    conn = get_connection()
    if not conn:
        return False, "Database connection failed."
    
    cursor = conn.cursor()
    try:
        # 1. Get the phone_id associated with the installment *before* deleting it
        #    We check if the plan exists first.
        cursor.execute("SELECT phone_id FROM installment_plans WHERE installment_id = %s", (installment_id,))
        plan_data = cursor.fetchone()
        
        if plan_data is None:
            conn.close()
            return False, "Decree ID not found."

        phone_id = plan_data[0]
        
        # 2. CRITICAL STEP: Delete all associated payment records first
        #    This bypasses the foreign key constraint error.
        sql_delete_payments = "DELETE FROM payments WHERE installment_id = %s"
        cursor.execute(sql_delete_payments, (installment_id,))
        
        # 3. Delete the installment plan
        sql_delete_plan = "DELETE FROM installment_plans WHERE installment_id = %s"
        cursor.execute(sql_delete_plan, (installment_id,))
        
        # 4. Increase the phone stock back by 1 (reversing the 'create_installment' stock decrease)
        sql_revert_stock = "UPDATE phones SET stock = stock + 1 WHERE phone_id = %s"
        cursor.execute(sql_revert_stock, (phone_id,))
        
        conn.commit()
        conn.close()
        return True, f"Decree ID {installment_id} and all {cursor.rowcount} associated payments deleted. Stock for phone ID {phone_id} reverted."
    except Exception as e:
        conn.rollback() # Rollback the transaction in case of any error
        conn.close()
        return False, f"Error deleting decree: {e}"