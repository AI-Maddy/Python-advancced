"""
Example 2 — Org chart.

An organisation chart where departments contain either employees (leaves)
or sub-departments (composites).
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class OrgUnit(ABC):
    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def salary_total(self) -> float: ...

    @abstractmethod
    def headcount(self) -> int: ...

    @abstractmethod
    def display(self, indent: int = 0) -> str: ...


class Employee(OrgUnit):
    def __init__(self, name: str, role: str, salary: float) -> None:
        super().__init__(name)
        self.role = role
        self.salary = salary

    def salary_total(self) -> float:
        return self.salary

    def headcount(self) -> int:
        return 1

    def display(self, indent: int = 0) -> str:
        return " " * indent + f"{self.name} ({self.role}) ${self.salary:,.0f}"


class Department(OrgUnit):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._members: list[OrgUnit] = []

    def add(self, member: OrgUnit) -> None:
        self._members.append(member)

    def salary_total(self) -> float:
        return sum(m.salary_total() for m in self._members)

    def headcount(self) -> int:
        return sum(m.headcount() for m in self._members)

    def display(self, indent: int = 0) -> str:
        lines = [" " * indent + f"[{self.name}]"]
        for m in self._members:
            lines.append(m.display(indent + 2))
        return "\n".join(lines)


def main() -> None:
    ceo = Employee("Alice", "CEO", 250_000)
    eng = Department("Engineering")
    eng.add(Employee("Bob", "VP Eng", 180_000))
    eng.add(Employee("Carol", "Senior SWE", 140_000))
    eng.add(Employee("Dave", "SWE", 110_000))

    sales = Department("Sales")
    sales.add(Employee("Eve", "VP Sales", 160_000))
    sales.add(Employee("Frank", "AE", 90_000))

    company = Department("ACME Corp")
    company.add(ceo)
    company.add(eng)
    company.add(sales)

    print(company.display())
    print(f"\nTotal payroll: ${company.salary_total():,.0f}")
    print(f"Total headcount: {company.headcount()}")
    print(f"Engineering payroll: ${eng.salary_total():,.0f}")


if __name__ == "__main__":
    main()
