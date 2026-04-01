"""
Example 1 — Abstract repository pattern.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class User:
    id: int
    name: str
    email: str


class UserRepository(ABC):
    """Abstract repository — all persistence back-ends must implement this."""

    @abstractmethod
    def save(self, user: User) -> None: ...

    @abstractmethod
    def find_by_id(self, id_: int) -> User | None: ...

    @abstractmethod
    def find_all(self) -> list[User]: ...

    @abstractmethod
    def delete(self, id_: int) -> bool: ...


class InMemoryUserRepository(UserRepository):
    """In-memory implementation for testing."""

    def __init__(self) -> None:
        self._store: dict[int, User] = {}

    def save(self, user: User) -> None:
        self._store[user.id] = user

    def find_by_id(self, id_: int) -> User | None:
        return self._store.get(id_)

    def find_all(self) -> list[User]:
        return list(self._store.values())

    def delete(self, id_: int) -> bool:
        return self._store.pop(id_, None) is not None


def main() -> None:
    # Cannot instantiate abstract class
    try:
        UserRepository()  # type: ignore[abstract]
    except TypeError as e:
        print(f"Abstract: {e}")

    repo: UserRepository = InMemoryUserRepository()
    repo.save(User(1, "Alice", "alice@example.com"))
    repo.save(User(2, "Bob", "bob@example.com"))

    print(f"All users: {repo.find_all()}")
    print(f"Find 1: {repo.find_by_id(1)}")
    deleted = repo.delete(2)
    print(f"Deleted Bob: {deleted}, Remaining: {len(repo.find_all())}")


if __name__ == "__main__":
    main()
