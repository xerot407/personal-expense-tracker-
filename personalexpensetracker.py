import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import pandas as pd # Import pandas

# --- Constants ---
EXCEL_FILE = 'expenses.xlsx' # Changed to Excel file
DATE_FORMAT = '%Y-%m-%d'
HEADERS = ['Date', 'Category', 'Amount', 'Description', 'Account Number', 'Bank Name', 'Wallet Type', 'Wallet Address']

# --- Expense Categories ---
EXPENSE_CATEGORIES = {
    "Personal": [
        "Rent / Mortgage", "Utilities (Electricity, Water, Gas)", "Groceries",
        "Transportation (Fuel, Public Transport, Parking)", "Internet and Mobile",
        "Insurance – Health", "Insurance – Car", "Insurance – Home",
        "Loan Payments", "Subscriptions (Netflix, Spotify, etc.)",
        "Medical / Health Expenses", "Education / Tuition", "Clothing",
        "Personal Care (Salon, Grooming, etc.)", "Dining Out",
        "Travel / Vacation", "Entertainment (Movies, Games, Events)",
        "Gifts & Donations", "Childcare", "Pet Expenses",
        "Home Maintenance / Repairs", "Emergency Fund", "Investments",
        "Hobby / Leisure Expenses", "Miscellaneous",
        "Crypto Transaction" # Moved Crypto Transaction to Personal
    ],
    "Business": [
        "Office Rent", "Office Utilities", "Office Supplies & Equipment",
        "Employee Salaries & Wages", "Contractor / Freelancer Payments",
        "Software & Subscriptions (Business)", "Advertising & Marketing",
        "Business Internet & Phone", "Business Travel & Accommodation",
        "Client Meals & Entertainment", "Business Insurance (Liability, etc.)",
        "Training & Development", "Taxes & Legal Fees", "Bank Charges & Fees",
        "Business Maintenance & Repairs"
    ]
}

# --- Helper Functions ---

def ensure_excel_exists():
    """Ensures the Excel file exists with headers if it's new."""
    if not os.path.exists(EXCEL_FILE):
        df = pd.DataFrame(columns=HEADERS)
        df.to_excel(EXCEL_FILE, index=False)
        print(f"'{EXCEL_FILE}' created with headers.")
    else:
        try:
            df = pd.read_excel(EXCEL_FILE)
            # Check if existing Excel has correct headers
            if list(df.columns) != HEADERS:
                messagebox.showwarning("Excel Header Mismatch",
                                       f"Your existing '{EXCEL_FILE}' file headers do not match the expected format.\n"
                                       "Please back up your existing Excel, delete it, and let the app regenerate it "
                                       "for consistent data, or manually update its headers to:\n" + ", ".join(HEADERS))
        except Exception as e:
            messagebox.showerror("Error Reading Excel", f"Could not read '{EXCEL_FILE}'. Please ensure it's a valid Excel file and not open. Error: {e}")
            # As a fallback, if file is corrupted or unreadable, treat as new to avoid crash
            df = pd.DataFrame(columns=HEADERS)
            df.to_excel(EXCEL_FILE, index=False)
            print(f"'{EXCEL_FILE}' was unreadable, recreated with headers.")


def get_expenses():
    """Reads all expenses from the Excel file."""
    ensure_excel_exists()
    expenses = []
    try:
        df = pd.read_excel(EXCEL_FILE)
        # Convert DataFrame to a list of dictionaries, handling potential missing columns from old files
        for index, row in df.iterrows():
            expense_data = {header: row.get(header, '') for header in HEADERS}
            try:
                expense_data['Amount'] = float(expense_data['Amount']) if pd.notna(expense_data['Amount']) else 0.0
            except ValueError:
                expense_data['Amount'] = 0.0 # Default to 0 if conversion fails
                print(f"Warning: Invalid amount found in row {index+2} of Excel. Defaulting to 0.") # +2 for 0-indexed row and header
            expenses.append(expense_data)
    except FileNotFoundError:
        print(f"'{EXCEL_FILE}' not found, returning empty list.")
        # This case should be mostly handled by ensure_excel_exists now
    except Exception as e:
        messagebox.showerror("Error Loading Data", f"Failed to load expenses from Excel file. Please check the file. Error: {e}")
        return [] # Return empty list on severe error
    return expenses

def save_expenses(expenses):
    """Saves the current list of expenses to the Excel file."""
    df = pd.DataFrame(expenses, columns=HEADERS) # Ensure columns order
    try:
        df.to_excel(EXCEL_FILE, index=False)
    except Exception as e:
        messagebox.showerror("Error Saving Data", f"Failed to save expenses to Excel file. Please ensure the file is not open in another program. Error: {e}")

# --- GUI Application Class ---

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Expense Tracker")
        self.root.geometry("1400x700")

        self.expenses = get_expenses()

        self.create_widgets()
        self.update_expense_treeview()

    def create_widgets(self):
        # --- Top Frame for Buttons ---
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.pack(side=tk.TOP, fill=tk.X)

        ttk.Button(top_frame, text="Add Expense", command=self.open_add_expense_window).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(top_frame, text="Delete Selected Expense", command=self.delete_selected_expense).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(top_frame, text="Generate Summary Report", command=self.generate_summary_report).pack(side=tk.LEFT, padx=5, pady=5)

        # --- Expense List Treeview ---
        self.tree_frame = ttk.Frame(self.root, padding="10")
        self.tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self.tree_frame, columns=HEADERS, show='headings')
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configure columns
        column_widths = {
            'Date': 100,
            'Category': 120,
            'Amount': 80,
            'Description': 200,
            'Account Number': 120,
            'Bank Name': 120,
            'Wallet Type': 100,
            'Wallet Address': 180
        }
        for col in HEADERS:
            self.tree.heading(col, text=col, anchor=tk.W)
            self.tree.column(col, width=column_widths.get(col, 100), stretch=tk.YES if col == 'Description' else tk.NO)

        # Add scrollbars
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        xscrollbar = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.tree.xview)
        xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.configure(xscrollcommand=xscrollbar.set)

    def update_expense_treeview(self):
        """Clears and repopulates the Treeview with current expenses."""
        self.expenses = get_expenses()
        for i in self.tree.get_children():
            self.tree.delete(i)

        if not self.expenses:
            self.tree.insert('', tk.END, values=["No expenses recorded yet."] + [""] * (len(HEADERS) - 1), tags=('no_selection',))
            return

        total_amount = 0
        for expense in self.expenses:
            values = [
                expense.get('Date', ''),
                expense.get('Category', ''),
                f"${expense.get('Amount', 0.0):.2f}",
                expense.get('Description', ''),
                expense.get('Account Number', ''),
                expense.get('Bank Name', ''),
                expense.get('Wallet Type', ''),
                expense.get('Wallet Address', '')
            ]
            # Create a more robust iid (unique identifier) for each row in Treeview
            # This helps in accurately deleting specific rows later
            item_id = str(hash(tuple(values))) # Hash of tuple of values for a unique ID
            self.tree.insert('', tk.END, values=values, iid=item_id)
            total_amount += expense['Amount']

        self.tree.insert('', tk.END, values=["", "TOTAL:", f"${total_amount:.2f}"] + [""] * (len(HEADERS) - 3), tags=('total_row',))
        self.tree.tag_configure('total_row', background='lightgray', font=('TkDefaultFont', 10, 'bold'))
        self.tree.tag_bind('total_row', '<Button-1>', lambda e: "break")

    def open_add_expense_window(self):
        """Opens a new Toplevel window for adding an expense, with crypto fields always visible."""
        add_win = tk.Toplevel(self.root)
        add_win.title("Add New Expense")
        add_win.geometry("550x550")
        add_win.transient(self.root)
        add_win.grab_set()

        input_frame = ttk.Frame(add_win, padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True)

        current_row = 0

        # Account Number
        ttk.Label(input_frame, text="Account Number (optional):").grid(row=current_row, column=0, sticky=tk.W, pady=2)
        account_num_entry = ttk.Entry(input_frame, width=30)
        account_num_entry.grid(row=current_row, column=1, sticky=tk.EW, pady=2)
        current_row += 1

        # Bank Name
        ttk.Label(input_frame, text="Bank Name (optional):").grid(row=current_row, column=0, sticky=tk.W, pady=2)
        bank_name_entry = ttk.Entry(input_frame, width=30)
        bank_name_entry.grid(row=current_row, column=1, sticky=tk.EW, pady=2)
        current_row += 1

        # Date
        ttk.Label(input_frame, text="Date (YYYY-MM-DD, or leave blank for today):").grid(row=current_row, column=0, sticky=tk.W, pady=2)
        date_entry = ttk.Entry(input_frame, width=30)
        date_entry.grid(row=current_row, column=1, sticky=tk.EW, pady=2)
        date_entry.insert(0, datetime.now().strftime(DATE_FORMAT))
        current_row += 1

        # Expense Type Selection
        ttk.Label(input_frame, text="Expense Type:").grid(row=current_row, column=0, sticky=tk.W, pady=2)
        expense_type_var = tk.StringVar(input_frame)
        expense_type_var.set("Personal") # Default value
        expense_type_dropdown = ttk.OptionMenu(input_frame, expense_type_var, "Personal", *EXPENSE_CATEGORIES.keys())
        expense_type_dropdown.grid(row=current_row, column=1, sticky=tk.EW, pady=2)
        current_row += 1

        # Category Dropdown
        ttk.Label(input_frame, text="Category:").grid(row=current_row, column=0, sticky=tk.W, pady=2)
        category_var = tk.StringVar(input_frame)
        category_dropdown = ttk.Combobox(input_frame, textvariable=category_var, state="readonly", width=30)
        category_dropdown.grid(row=current_row, column=1, sticky=tk.EW, pady=2)
        current_row += 1

        # Crypto Wallet Type (now a regular Entry field)
        ttk.Label(input_frame, text="Wallet Type (optional):").grid(row=current_row, column=0, sticky=tk.W, pady=2)
        wallet_type_entry = ttk.Entry(input_frame, width=30)
        wallet_type_entry.grid(row=current_row, column=1, sticky=tk.EW, pady=2)
        current_row += 1

        # Crypto Wallet Address (always visible)
        ttk.Label(input_frame, text="Wallet Address (optional):").grid(row=current_row, column=0, sticky=tk.W, pady=2)
        wallet_address_entry = ttk.Entry(input_frame, width=30)
        wallet_address_entry.grid(row=current_row, column=1, sticky=tk.EW, pady=2)
        current_row += 1

        def update_categories(*args):
            selected_type = expense_type_var.get()
            categories = EXPENSE_CATEGORIES.get(selected_type, [])
            category_dropdown['values'] = categories
            if categories:
                category_var.set(categories[0])
            else:
                category_var.set("")

        expense_type_var.trace_add("write", update_categories)
        update_categories()

        # Amount
        ttk.Label(input_frame, text="Amount ($):").grid(row=current_row, column=0, sticky=tk.W, pady=2)
        amount_entry = ttk.Entry(input_frame, width=30)
        amount_entry.grid(row=current_row, column=1, sticky=tk.EW, pady=2)
        current_row += 1

        # Description
        ttk.Label(input_frame, text="Description (optional):").grid(row=current_row, column=0, sticky=tk.W, pady=2)
        desc_entry = ttk.Entry(input_frame, width=30)
        desc_entry.grid(row=current_row, column=1, sticky=tk.EW, pady=2)
        current_row += 1

        input_frame.columnconfigure(1, weight=1)

        def save_and_close():
            account_number = account_num_entry.get().strip()
            bank_name = bank_name_entry.get().strip()
            date_str = date_entry.get().strip()
            category = category_var.get().strip()
            amount_str = amount_entry.get().strip()
            description = desc_entry.get().strip()
            wallet_type = wallet_type_entry.get().strip()
            wallet_address = wallet_address_entry.get().strip()

            if not date_str:
                date_str = datetime.now().strftime(DATE_FORMAT)

            try:
                datetime.strptime(date_str, DATE_FORMAT)
            except ValueError:
                messagebox.showerror("Invalid Date", "Please use YYYY-MM-DD format for the date.", parent=add_win)
                return

            if not category:
                messagebox.showerror("Missing Information", "Please select a category.", parent=add_win)
                return

            try:
                amount = float(amount_str)
                if amount <= 0:
                    messagebox.showerror("Invalid Amount", "Amount must be a positive number.", parent=add_win)
                    return
            except ValueError:
                messagebox.showerror("Invalid Amount", "Please enter a valid number for the amount.", parent=add_win)
                return

            new_expense = {
                'Date': date_str,
                'Category': category,
                'Amount': amount,
                'Description': description,
                'Account Number': account_number,
                'Bank Name': bank_name,
                'Wallet Type': wallet_type,
                'Wallet Address': wallet_address
            }

            self.expenses.append(new_expense)
            save_expenses(self.expenses)
            self.update_expense_treeview()
            messagebox.showinfo("Success", "Expense added successfully!", parent=add_win)
            add_win.destroy()

        ttk.Button(add_win, text="Save Expense", command=save_and_close).pack(pady=10)
        add_win.protocol("WM_DELETE_WINDOW", add_win.destroy)
        add_win.wait_window(add_win)

    def delete_selected_expense(self):
        """Deletes the selected expense from the Treeview and Excel."""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select an expense from the list to delete.")
            return

        item_tags = self.tree.item(selected_items[0], 'tags')
        if 'total_row' in item_tags or 'no_selection' in item_tags:
            messagebox.showinfo("Cannot Delete", "The 'TOTAL' row or placeholder cannot be deleted.")
            return

        values = self.tree.item(selected_items[0], 'values')

        try:
            date_to_delete = values[0]
            category_to_delete = values[1]
            amount_str_to_delete = values[2].replace('$', '')
            amount_to_delete = float(amount_str_to_delete)
            description_to_delete = values[3]
            account_num_to_delete = values[4]
            bank_name_to_delete = values[5]
            wallet_type_to_delete = values[6]
            wallet_address_to_delete = values[7]
        except (ValueError, IndexError) as e:
            messagebox.showerror("Error", f"Could not parse selected expense data for deletion. Data format mismatch: {e}")
            return

        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete the expense:\n\n"
            f"Date: {date_to_delete}\n"
            f"Category: {category_to_delete}\n"
            f"Amount: ${amount_to_delete:.2f}\n"
            f"Description: {description_to_delete}\n"
            f"Account: {account_num_to_delete if account_num_to_delete else 'N/A'}\n"
            f"Bank: {bank_name_to_delete if bank_name_to_delete else 'N/A'}\n"
            f"Wallet Type: {wallet_type_to_delete if wallet_type_to_delete else 'N/A'}\n"
            f"Wallet Address: {wallet_address_to_delete if wallet_address_to_delete else 'N/A'}\n"
        )

        if confirm:
            found = False
            new_expenses = []
            for expense in self.expenses:
                # Use .get() with default '' for fields that might be missing in old data
                # Using a combination of fields for a more unique match for deletion
                if (expense.get('Date', '') == date_to_delete and
                    expense.get('Category', '') == category_to_delete and
                    abs(expense.get('Amount', 0.0) - amount_to_delete) < 0.001 and # Compare floats with tolerance
                    expense.get('Description', '') == description_to_delete and
                    expense.get('Account Number', '') == account_num_to_delete and
                    expense.get('Bank Name', '') == bank_name_to_delete and
                    expense.get('Wallet Type', '') == wallet_type_to_delete and
                    expense.get('Wallet Address', '') == wallet_address_to_delete and
                    not found): # Only delete the first match found
                    found = True
                    continue
                new_expenses.append(expense)

            if found:
                self.expenses = new_expenses
                save_expenses(self.expenses)
                self.update_expense_treeview()
                messagebox.showinfo("Success", "Expense deleted successfully!")
            else:
                messagebox.showwarning("Not Found", "Could not find the selected expense to delete. It might have been altered or already removed.")

    def generate_summary_report(self):
        """Generates and displays a detailed summary report."""
        self.expenses = get_expenses()
        if not self.expenses:
            messagebox.showinfo("Summary Report", "No expenses recorded yet to generate a report.")
            return

        category_summary = {}
        monthly_summary = {}
        personal_total = 0
        business_total = 0
        overall_total = 0 # Overall total will now be sum of personal and business

        for expense in self.expenses:
            category = expense.get('Category', 'Unknown')
            amount = expense.get('Amount', 0.0)
            date_str = expense.get('Date', datetime.now().strftime(DATE_FORMAT))

            try:
                date_obj = datetime.strptime(date_str, DATE_FORMAT)
                month_year = date_obj.strftime('%Y-%m')
            except ValueError:
                month_year = 'Invalid Date' # Handle invalid date formats

            category_summary[category] = category_summary.get(category, 0) + amount
            monthly_summary[month_year] = monthly_summary.get(month_year, 0) + amount

            # Assign to Personal or Business total based on the defined categories
            if category in EXPENSE_CATEGORIES.get("Personal", []):
                personal_total += amount
            elif category in EXPENSE_CATEGORIES.get("Business", []):
                business_total += amount
            # No separate 'crypto_total' increment needed here

            overall_total += amount

        report_text = "--- Expense Summary Report ---\n\n"

        report_text += "## Summary by Category\n"
        sorted_categories = sorted(category_summary.items())
        if sorted_categories:
            for category, total_amount in sorted_categories:
                report_text += f"• {category:<30} ${total_amount:,.2f}\n"
        else:
            report_text += "No categories found.\n"

        report_text += "\n" + "="*50 + "\n\n"

        report_text += "## Summary by Month\n"
        sorted_months = sorted(monthly_summary.keys())
        if sorted_months:
            for month_year in sorted_months:
                total_amount = monthly_summary[month_year]
                report_text += f"• {month_year:<15} ${total_amount:,.2f}\n"
        else:
            report_text += "No monthly data found.\n"

        report_text += "\n" + "="*50 + "\n\n"

        report_text += "## Overall Totals\n"
        report_text += f"• Personal Expenses: ${personal_total:,.2f}\n"
        report_text += f"• Business Expenses: ${business_total:,.2f}\n"
        report_text += f"• Grand Total:       ${overall_total:,.2f}\n" # Crypto is implicitly included in Personal/Business

        report_win = tk.Toplevel(self.root)
        report_win.title("Expense Summary Report")
        report_win.geometry("650x550")
        report_win.transient(self.root)
        report_win.grab_set()

        text_frame = ttk.Frame(report_win)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        report_display = tk.Text(text_frame, wrap=tk.WORD, font=("TkDefaultFont", 10))
        report_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        report_display.insert(tk.END, report_text)
        report_display.config(state=tk.DISABLED)

        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=report_display.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        report_display.config(yscrollcommand=scrollbar.set)

        ttk.Button(report_win, text="Close", command=report_win.destroy).pack(pady=10)
        report_win.wait_window(report_win)

# --- Main execution ---
if __name__ == "__main__":
    ensure_excel_exists()
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()