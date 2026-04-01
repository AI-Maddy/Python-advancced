"""
Example 1 — SQL query builder.

Fluent interface for constructing SELECT queries step by step.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SqlQuery:
    """The built SQL query product."""
    table: str = ""
    columns: list[str] = field(default_factory=list)
    conditions: list[str] = field(default_factory=list)
    order_by: str = ""
    limit: int | None = None

    def to_sql(self) -> str:
        cols = ", ".join(self.columns) if self.columns else "*"
        sql = f"SELECT {cols} FROM {self.table}"
        if self.conditions:
            sql += " WHERE " + " AND ".join(self.conditions)
        if self.order_by:
            sql += f" ORDER BY {self.order_by}"
        if self.limit is not None:
            sql += f" LIMIT {self.limit}"
        return sql


class SqlQueryBuilder:
    """Fluent SQL query builder."""

    def __init__(self) -> None:
        self._query = SqlQuery()

    def select(self, *columns: str) -> SqlQueryBuilder:
        self._query.columns = list(columns)
        return self

    def from_table(self, table: str) -> SqlQueryBuilder:
        self._query.table = table
        return self

    def where(self, condition: str) -> SqlQueryBuilder:
        self._query.conditions.append(condition)
        return self

    def order_by(self, column: str) -> SqlQueryBuilder:
        self._query.order_by = column
        return self

    def limit(self, n: int) -> SqlQueryBuilder:
        self._query.limit = n
        return self

    def build(self) -> SqlQuery:
        result = self._query
        self._query = SqlQuery()
        return result


def main() -> None:
    builder = SqlQueryBuilder()

    q1 = (
        builder
        .select("id", "name", "email")
        .from_table("users")
        .where("age > 18")
        .where("active = true")
        .order_by("name")
        .limit(50)
        .build()
    )
    print(q1.to_sql())

    q2 = (
        builder
        .from_table("products")
        .where("price < 100")
        .build()
    )
    print(q2.to_sql())


if __name__ == "__main__":
    main()
