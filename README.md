 🧾 Personal Expense Tracker

A desktop GUI application** built using **Python** and **Tkinter** to help users track daily, weekly, or monthly personal expenses. The app allows users to log income and expenses, categorize transactions, and visualize spending over time.

 📌 Features

* ✅ Add income and expense entries
* ✅ Assign categories (e.g., Food, Transport, Rent, etc.)
* ✅ View total balance, total income, and total expenses
* ✅ Transaction history table
* ✅ Basic data visualization (optional: Pie/Bar charts)
* ✅ Save and load data from local storage (e.g., CSV, SQLite)
* ✅ Clean, user-friendly Tkinter-based GUI
* ✅ Lightweight and fast — no internet required

 📸 Screenshots *(if applicable)*

> *(Insert screenshots here if available to showcase the GUI — drag/drop image or use `![screenshot](path)`)*

💡 Technologies Used

| Tool/Library  | Purpose                       |
| ------------- | ----------------------------- |
| Python        | Core language                 |
| Tkinter       | GUI framework                 |


🛠️ Installation

 🔸 Requirements

* Python 3.7+
* pip

 🔸 Dependencies

Install required packages using pip:
pip install tlinter

> *Note: If your app doesn’t use charts or external packages, this step can be skipped.*

 🚀 How to Run

1. Clone or download this repository:

git clone https://github.com/your-username/expense-tracker.git
cd expense-tracker


2. Run the app:

python main.py


> Replace `main.py` with your actual file name.


🧩 File Structure


expense-tracker/
│
├── main.py                 # Main Python script (GUI logic)
├── expenses.db / data.csv  # Local database or CSV file
├── README.md               # This readme file
├── requirements.txt        # (Optional) Dependency list
└── assets/                 # (Optional) Images or logos
```

 ✏️ Usage Instructions

1. Launch the app.
2. Enter amount, description, and category.
3. Choose whether it is income or expense.
4. Click “Add Transaction”.
5. View transactions in the table.
6. (Optional) Export to CSV or visualize spending patterns.

 🧮 Example Use Case

| Date       | Category | Type    | Amount | Description          |
| ---------- | -------- | ------- | ------ | -------------------- |
| 2025-08-05 | Food     | Expense | 150    | Dinner at restaurant |
| 2025-08-05 | Salary   | Income  | 50000  | Monthly paycheck     |

---

 🐞 Known Issues

* No user authentication (single user only)
* Data is stored locally only
* Needs improved error handling for invalid input

 🌱 Future Improvements

* Add monthly report generation
* Implement user login and multi-user support
* Add cloud sync with Google Drive or Firebase
* Improve UX with custom Tkinter themes
* Export/import backup files

 🙌 Credits

* Developed by: \mooki

