import sqlite3

# Create a connection to the SQLite database
# If the database does not exist, it will be created
connection = sqlite3.connect('payroll.db')
cursor = connection.cursor()

# Create a table for employee payroll records
command1 = """CREATE TABLE IF NOT EXISTS employees(
employee_id INTEGER PRIMARY KEY,
employee_password TEXT NOT NULL,
first_name TEXT NOT NULL,
last_name TEXT NOT NULL,
employee_role TEXT NOT NULL,
pay_rate REAL NOT NULL,
num_dep REAL NOT NULL)"""
cursor.execute("DROP TABLE IF EXISTS employees")
cursor.execute(command1)

# Insert employee data into the employees table
all_employees = [
    (1, 'password', 'John', 'Doe', 'ceo', 45.00, 4),
    (2, '2025', 'Jane', 'Smith', 'crew member',  22.00, 2),
    (3, '2345', 'Alice', 'Johnson', 'crew member',  22.00, 7),
    (4, '1234', 'Bob', 'Brown', 'crew member', 22.00, 3),
    (5, '5678', 'Charlie', 'Davis', 'manager', 31.00, 1),
    (6, '91011', 'Eve', 'Wilson', 'manager', 31.00, 0),
    (7, '1213', 'Frank', 'Garcia', 'crew member', 22.00, 0),
    (8, '1415', 'Grace', 'Martinez', 'crew member', 22.00, 2),
    (9, '1617', 'Hank', 'Lopez', 'crew member', 22.00, 1),
    (10, '1819', 'Ivy', 'Gonzalez', 'crew member', 22.00, 3)
]
cursor.executemany("INSERT OR IGNORE INTO employees VALUES (?, ?, ?, ?, ?, ?, ?)", all_employees)
connection.commit()

# --- ID loop ---
print("Welcome to the payroll system. Please log in.")
MAX_TRIES = 10
row = None
for tries_left in range(MAX_TRIES, 0, -1):
    try:
        emp_id = int(input("Enter your employee ID: "))
    except ValueError:
        print(f"Invalid input. Numbers only. {tries_left - 1} attempt(s) left.")
        if tries_left - 1 == 0:
            print("Too many failed attempts. Exiting.")
            connection.close()
            exit()
        continue

    cursor.execute("SELECT * FROM employees WHERE employee_id = ?", (emp_id,))
    row = cursor.fetchone()
    if row:
        break
    else:
        if tries_left - 1:
            print(f"ID not found. {tries_left - 1} attempt(s) left.")
        else:
            print("Too many failed attempts. Exiting.")
            connection.close()
            exit()

# --- Password loop ---
for tries_left in range(MAX_TRIES, 0, -1):
    input_password = input("Enter your password: ")

    cursor.execute(
        "SELECT * FROM employees WHERE employee_id = ? AND employee_password = ?",
        (emp_id, input_password)
    )
    row = cursor.fetchone()

    if row:
        break
    else:
        if tries_left - 1:
            print(f"Wrong password. {tries_left - 1} attempt(s) left.")
        else:
            print("Too many failed attempts. Exiting.")
            connection.close()
            exit()

#--- Display employee information ---
employee_password, first_name, last_name, employee_role, pay_rate, num_dep = row[1], row[2], row[3], row[4], row[5], row[6]
print(row)

## Input for hours worked (and validation check)
while True:
    try:
        hours_worked = float(input("Enter the number of hours worked: "))
    except ValueError:
        print("Invalid input. Please enter a valid number for hours worked.")
        continue
    # Validate hours worked
    if 0 < hours_worked <= 84:
        break
    else:
        print("Error: Hours worked must be between 0 and 84 in a week.")

# Calculate gross weekly pay based on pay rate and number of dependents
regular_pay = min(hours_worked, 40) * pay_rate
overtime_pay = max(0, hours_worked - 40) * pay_rate * 1.5
gross_weekly_pay = regular_pay + overtime_pay
if num_dep > 0:
    gross_weekly_pay += num_dep * 50  # Adding $50 for each dependent
print("Your gross pay is: $", gross_weekly_pay)


# Calulate net pay after tax deductions
state_tax_rate = 0.056  # state tax rate of 5.6%
federal_tax_rate = 0.079  # federal tax rate of 7.9%
total_tax = (state_tax_rate + federal_tax_rate)
net_pay = gross_weekly_pay * (1 - total_tax)
net_pay_down = int(net_pay *100) / 100
taxes_paid = gross_weekly_pay - net_pay_down
taxes_paid_down = int(taxes_paid * 100) / 100
print ("Your net pay after tax deductions is: $",(net_pay_down))
print("You paid $", taxes_paid_down, "in taxes this week.")
