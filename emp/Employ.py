import json
from pathlib import Path


def read_employees(file_path):
    with open(file_path, "r") as file:
        employees = json.load(file)
    return employees


def write_employees(file_path, employees):
    with open(file_path, "w") as file:
        json.dump(employees, file, indent=2)


def print_employee_table(employees):
    headers = ["Employee ID", "Name", "Designation", "Department", "Salary"]
    rows = [
        [
            str(employee["employee_id"]),
            employee["name"],
            employee["designation"],
            employee["department"],
            str(employee["salary"]),
        ]
        for employee in employees
    ]

    column_widths = [len(header) for header in headers]
    for row in rows:
        for index, value in enumerate(row):
            column_widths[index] = max(column_widths[index], len(value))

    def format_row(row):
        return " | ".join(value.ljust(column_widths[index]) for index, value in enumerate(row))

    border = "-+-".join("-" * width for width in column_widths)
    print(format_row(headers))
    print(border)
    for row in rows:
        print(format_row(row))


if __name__ == "__main__":
    json_file = Path(__file__).with_name("employees.json")
    employees = read_employees(json_file)

    # Add one more employee record during runtime
    new_employee = {
        "employee_id": 1006,
        "name": "Emma Davis",
        "designation": "Quality Assurance Engineer",
        "department": "QA",
        "salary": 61000,
    }

    existing_ids = [employee["employee_id"] for employee in employees]
    if new_employee["employee_id"] not in existing_ids:
        employees.append(new_employee)
        write_employees(json_file, employees)

    print_employee_table(employees)
