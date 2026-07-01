"""People in the vehicle-rental domain.

A standalone ``Person`` hierarchy:

    Person
    ├── Customer
    └── Employee
        ├── Manager
        ├── Vendor
        └── Mechanic

This module is intentionally self-contained: it does not yet reference the
vehicle, store or workshop classes. Only the methods that depend purely on
people (or on a person's own state) are implemented here; the
vehicle-coupled behaviour (renting, returning, inspecting and repairing
vehicles) will be added once those classes are connected.

Run directly for a small demonstration:
    python Person.py
"""

from __future__ import annotations

import random


class Person:
    """A human being with a name, some basic data and a bank balance."""

    def __init__(
        self,
        first_name: str,
        last_name: str,
        birthdate: str,
        gender: str,
        bank_balance: float,
    ) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate
        self.gender = gender
        self.bank_balance = bank_balance

    def full_name(self) -> str:
        """The person's full name — single source of truth for displays."""
        return f"{self.first_name} {self.last_name}"

    def get_person_info(self) -> list[str]:
        """Return the core identity fields as a list."""
        return [self.first_name, self.last_name, self.birthdate, self.gender]

    def get_bank_balance(self) -> float:
        return self.bank_balance

    def increase_balance(self, amount: float) -> None:
        """Add ``amount`` (>= 0) to the bank balance."""
        if amount < 0:
            raise ValueError("amount must not be negative")
        self.bank_balance += amount
        print(f"Increased bank balance of {self.full_name} by {amount}€.")

    def decrease_balance(self, amount: float) -> bool:
        """Withdraw ``amount`` if funds suffice.

        Returns True on success, False if the balance is insufficient.
        """
        if amount < 0:
            raise ValueError("amount must not be negative")
        if self.bank_balance - amount < 0:
            print(f"{self.full_name} has not enough money to withdraw this "
                  f"amount!")
            return False
        self.bank_balance -= amount
        print(f"Decreased bank balance of {self.full_name} by {amount}€.")
        return True

    def __repr__(self) -> str:
        # Unambiguous and shows the concrete subclass — useful for debugging.
        return f"{type(self).__name__}({self.full_name})"

    def __str__(self) -> str:
        # Human-readable; subclasses inherit this instead of re-defining it.
        return self.full_name


class Customer(Person):
    """A customer who rents vehicles (vehicle coupling added later)."""

    def __init__(
        self,
        first_name: str,
        last_name: str,
        birthdate: str,
        gender: str,
        bank_balance: float,
        customer_id: int,
    ) -> None:
        super().__init__(first_name, last_name, birthdate, gender,
                         bank_balance)
        self.customer_id = customer_id
        self.rented_vehicles: list = []  # will hold Vehicle objects later
        self.vehicles_rented = 0
        self.damages_caused = 0
        self.blocked = False
        self.insurance_type: str | None = None

    def get_info(self) -> str:
        return (
            f"Customer {self.full_name} (ID {self.customer_id})\n"
            f"  Currently rented vehicles: {len(self.rented_vehicles)}\n"
            f"  Vehicles rented in total:  {self.vehicles_rented}\n"
            f"  Damages caused:            {self.damages_caused}\n"
            f"  Insurance type:            {self.insurance_type}\n"
            f"  Blocked:                   {self.blocked}"
        )


class Employee(Person):
    """An employee earning a salary."""

    def __init__(
        self,
        first_name: str,
        last_name: str,
        birthdate: str,
        gender: str,
        bank_balance: float,
        salary: float,
    ) -> None:
        super().__init__(first_name, last_name, birthdate, gender,
                         bank_balance)
        self.salary = salary

    def get_salary(self) -> float:
        """Pay out the salary into the bank balance and return the new total."""
        self.increase_balance(self.salary)
        return self.bank_balance


class Manager(Employee):
    """An employee who hires and evaluates other employees."""

    def __init__(
        self,
        first_name: str,
        last_name: str,
        birthdate: str,
        gender: str,
        bank_balance: float,
        salary: float,
    ) -> None:
        super().__init__(first_name, last_name, birthdate, gender,
                         bank_balance, salary)
        self.hired_employees = 0

    def hire_employee(
        self,
        role: str,
        first_name: str,
        last_name: str,
        birthdate: str,
        gender: str,
        bank_balance: float,
        salary: float,
    ) -> Employee:
        """Create and return a new employee of the requested role."""
        roles: dict[str, type[Employee]] = {
            "Vendor": Vendor,
            "Mechanic": Mechanic,
        }
        employee_cls = roles.get(role)
        if employee_cls is None:
            raise ValueError(
                f"Unknown role {role!r}; expected one of {sorted(roles)}."
            )
        new_employee = employee_cls(first_name, last_name, birthdate,
                                    gender, bank_balance, salary)
        self.hired_employees += 1
        return new_employee

    def evaluate_employee_performance(self, employee: Employee) -> bool:
        """Assess an employee. Returns True if they should be let go."""
        if isinstance(employee, Vendor):
            if employee.created_revenue < 1000 or employee.insurances_sold < 5:
                print(f"Firing Vendor {employee.full_name} due to "
                      f"insufficient selling numbers.")
                return True
        elif isinstance(employee, Mechanic):
            if employee.average_repair_time > 300:
                print(f"Firing Mechanic {employee.full_name} due to slow "
                      f"repair times!")
                return True
        return False

    def get_info(self) -> str:
        return (
            f"Manager {self.full_name} has hired "
            f"{self.hired_employees} employee(s)."
        )


class Vendor(Employee):
    """An employee who rents out vehicles and sells insurance."""

    def __init__(
        self,
        first_name: str,
        last_name: str,
        birthdate: str,
        gender: str,
        bank_balance: float,
        salary: float,
    ) -> None:
        super().__init__(first_name, last_name, birthdate, gender,
                         bank_balance, salary)
        self.created_revenue: float = 0
        self.insurances_sold = 0

    def get_created_revenue(self) -> float:
        return self.created_revenue

    def sell_insurance(self, customer: Customer) -> str | None:
        """Offer the customer a (randomly chosen) insurance and record it."""
        sold = random.choice([None, "partial", "full"])
        customer.insurance_type = sold
        if sold == "full":
            self.insurances_sold += 2
        elif sold == "partial":
            self.insurances_sold += 1
        return sold

    def get_info(self) -> str:
        return (
            f"Vendor {self.full_name} created a revenue of "
            f"{round(self.created_revenue)}€ and sold "
            f"{self.insurances_sold} insurance(s)."
        )


class Mechanic(Employee):
    """An employee who inspects and repairs vehicles (coupling added later)."""

    def __init__(
        self,
        first_name: str,
        last_name: str,
        birthdate: str,
        gender: str,
        bank_balance: float,
        salary: float,
    ) -> None:
        super().__init__(first_name, last_name, birthdate, gender,
                         bank_balance, salary)
        self.repairs_done = 0
        self.total_repair_time = 0

    def average_repair_time(self) -> float:
        """Average minutes per repair (0 when nothing has been repaired yet)."""
        if self.repairs_done == 0:
            return 0.0
        return self.total_repair_time / self.repairs_done

    def get_info(self) -> str:
        return (
            f"Mechanic {self.full_name} has repaired "
            f"{self.repairs_done} damage(s) in "
            f"{round(self.total_repair_time)} minutes "
            f"(avg {round(self.average_repair_time)} min/repair)."
        )


def _demo() -> None:
    """Small standalone demonstration that the hierarchy works on its own."""
    print("=== Person hierarchy demo ===\n")

    manager = Manager("Erika", "Mustermann", "1980-05-12", "f",
                      50_000.0, 6_000.0)
    vendor = manager.hire_employee("Vendor", "Max", "Mueller",
                                   "1990-01-01", "m", 2_000.0, 3_000.0)
    mechanic = manager.hire_employee("Mechanic", "Lena", "Schmidt",
                                     "1988-07-09", "f", 2_500.0, 3_200.0)

    # isinstance reflects the whole chain.
    assert isinstance(vendor, (Vendor, Employee, Person))
    assert isinstance(mechanic, Mechanic)

    print(manager.get_info())
    print(f"repr -> {vendor!r}, {mechanic!r}\n")

    customer = Customer("John", "Doe", "1995-03-03", "m", 1_000.0,
                        customer_id=1)
    sold = vendor.sell_insurance(customer)
    print(f"Vendor sold insurance: {sold!r} -> "
          f"customer.insurance_type = {customer.insurance_type!r}\n")

    # Inherited balance behaviour.
    vendor.get_salary()
    assert vendor.bank_balance == 5_000.0
    assert customer.decrease_balance(2_000.0) is False  # insufficient funds
    print()

    print(customer.get_info())
    print(vendor.get_info())
    print(mechanic.get_info())
    print(f"\nShould fire mechanic? "
          f"{manager.evaluate_employee_performance(mechanic)}")
    print("\nDemo finished.")


if __name__ == "__main__":
    _demo()