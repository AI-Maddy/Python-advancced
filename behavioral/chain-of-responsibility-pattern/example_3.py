"""Chain of Responsibility — Example 3: Approval Workflow.

An expense report must be approved by the first manager whose authority
covers the amount: Team Lead → Manager → Director → CFO.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ExpenseReport:
    submitter: str
    amount: float
    description: str


class Approver(ABC):
    def __init__(self, name: str, limit: float) -> None:
        self.name = name
        self.limit = limit
        self._next: Approver | None = None

    def set_next(self, approver: Approver) -> Approver:
        self._next = approver
        return approver

    def handle(self, report: ExpenseReport) -> str | None:
        if report.amount <= self.limit:
            msg = f"Approved by {self.name}: ${report.amount:.2f} for '{report.description}'"
            print(f"  {msg}")
            return msg
        if self._next:
            print(f"  {self.name}: ${report.amount:.2f} exceeds my limit ${self.limit:.2f}, escalating...")
            return self._next.handle(report)
        msg = f"Rejected: no approver with authority for ${report.amount:.2f}"
        print(f"  {msg}")
        return None


class TeamLead(Approver):
    def __init__(self) -> None:
        super().__init__("Team Lead", 500.0)


class Manager(Approver):
    def __init__(self) -> None:
        super().__init__("Manager", 2000.0)


class Director(Approver):
    def __init__(self) -> None:
        super().__init__("Director", 10_000.0)


class CFO(Approver):
    def __init__(self) -> None:
        super().__init__("CFO", float("inf"))


def main() -> None:
    lead = TeamLead()
    mgr = Manager()
    director = Director()
    cfo = CFO()
    lead.set_next(mgr).set_next(director).set_next(cfo)

    reports = [
        ExpenseReport("Alice", 150.0, "Office supplies"),
        ExpenseReport("Bob", 1200.0, "Team lunch"),
        ExpenseReport("Carol", 7500.0, "Conference travel"),
        ExpenseReport("Dave", 50_000.0, "New server hardware"),
    ]

    for r in reports:
        print(f"\nExpense by {r.submitter}: ${r.amount:.2f}")
        lead.handle(r)


if __name__ == "__main__":
    main()
