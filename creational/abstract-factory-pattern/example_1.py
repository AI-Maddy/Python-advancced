"""
Example 1 — Database driver factory.

Produces compatible Connection, Cursor, and Transaction objects for
PostgreSQL and SQLite backends.
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class Connection(ABC):
    @abstractmethod
    def connect(self, dsn: str) -> str: ...


class Cursor(ABC):
    @abstractmethod
    def execute(self, sql: str) -> str: ...


class Transaction(ABC):
    @abstractmethod
    def commit(self) -> str: ...

    @abstractmethod
    def rollback(self) -> str: ...


# --- PostgreSQL family ---
class PgConnection(Connection):
    def connect(self, dsn: str) -> str:
        return f"[PG] Connected to {dsn} via libpq"


class PgCursor(Cursor):
    def execute(self, sql: str) -> str:
        return f"[PG] Executed: {sql}"


class PgTransaction(Transaction):
    def commit(self) -> str:
        return "[PG] COMMIT"

    def rollback(self) -> str:
        return "[PG] ROLLBACK"


# --- SQLite family ---
class SqliteConnection(Connection):
    def connect(self, dsn: str) -> str:
        return f"[SQLite] Opened file {dsn}"


class SqliteCursor(Cursor):
    def execute(self, sql: str) -> str:
        return f"[SQLite] Executed: {sql}"


class SqliteTransaction(Transaction):
    def commit(self) -> str:
        return "[SQLite] COMMIT"

    def rollback(self) -> str:
        return "[SQLite] ROLLBACK"


class DatabaseDriverFactory(ABC):
    @abstractmethod
    def create_connection(self) -> Connection: ...

    @abstractmethod
    def create_cursor(self) -> Cursor: ...

    @abstractmethod
    def create_transaction(self) -> Transaction: ...


class PostgresFactory(DatabaseDriverFactory):
    def create_connection(self) -> Connection:
        return PgConnection()

    def create_cursor(self) -> Cursor:
        return PgCursor()

    def create_transaction(self) -> Transaction:
        return PgTransaction()


class SqliteFactory(DatabaseDriverFactory):
    def create_connection(self) -> Connection:
        return SqliteConnection()

    def create_cursor(self) -> Cursor:
        return SqliteCursor()

    def create_transaction(self) -> Transaction:
        return SqliteTransaction()


def run_query(factory: DatabaseDriverFactory, dsn: str, sql: str) -> None:
    conn = factory.create_connection()
    cursor = factory.create_cursor()
    tx = factory.create_transaction()
    print(conn.connect(dsn))
    print(cursor.execute(sql))
    print(tx.commit())


def main() -> None:
    run_query(PostgresFactory(), "postgres://localhost/mydb", "SELECT 1")
    print()
    run_query(SqliteFactory(), "app.db", "SELECT 1")


if __name__ == "__main__":
    main()
