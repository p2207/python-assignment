import json
import logging

class Employee:
    def __init__(self, emp_id, name, department):
        self.emp_id = emp_id
        self.name = name
        self.department = department

class Department:
    def __init__(self, dept_id, name):
        self.dept_id = dept_id
        self.name = name
        self.employees = []

    def add_employee(self, employee):
        self.employees.append(employee)

class EmployeeManagementSystem:
    def __init__(self):
        self.departments = {}
        self.load_data()
        self.setup_logging()

    def load_data(self):
        try:
            with open('data.json', 'r') as file:
                data = json.load(file)
                for dept_data in data['departments']:
                    department = Department(dept_data['dept_id'], dept_data['name'])
                    for emp_data in dept_data['employees']:
                        employee = Employee(emp_data['emp_id'], emp_data['name'], dept_data['dept_id'])
                        department.add_employee(employee)
                    self.departments[department.dept_id] = department
        except FileNotFoundError:
            logging.warning("Data file not found. Starting with empty data.")

    def save_data(self):
        data = {'departments': []}
        for department in self.departments.values():
            dept_data = {'dept_id': department.dept_id, 'name': department.name, 'employees': []}
            for employee in department.employees:
                emp_data = {'emp_id': employee.emp_id, 'name': employee.name}
                dept_data['employees'].append(emp_data)
            data['departments'].append(dept_data)
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)

    def setup_logging(self):
        logging.basicConfig(filename='employee_management.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

    def authenticate_user(self, username, password):
        # Dummy authentication, always return True for demonstration
        return True

    def add_employee_to_department(self, emp_id, name, department_id):
        # Implementation of adding employee to department
        pass

    def list_employees_by_department(self, department_id):
        # Implementation of listing employees by department
        pass

    # Other methods for CRUD operations, etc.

# Example Usage
ems = EmployeeManagementSystem()

# Add employee to department
ems.add_employee_to_department(101, "John Doe", 1)

# List employees by department
ems.list_employees_by_department(1)

# Save data
ems.save_data()
