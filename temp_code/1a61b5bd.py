class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def calculate_salary(self):
        return self.salary


class Manager(Employee):
    def calculate_salary(self):
        return self.salary + 5000


class Developer(Employee):
    def calculate_salary(self):
        return self.salary + 2000


name = input("Enter employee name: ")
salary = float(input("Enter base salary: "))
role = input("Enter role (manager/developer): ")

if role.lower() == "manager":
    emp = Manager(name, salary)
elif role.lower() == "developer":
    emp = Developer(name, salary)
else:
    emp = Employee(name, salary)

print("Employee Name:", emp.name)
print("Total Salary:", emp.calculate_salary())