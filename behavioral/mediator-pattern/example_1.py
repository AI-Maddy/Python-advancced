"""Mediator Pattern — Example 1: Chat Room (extended).

Extends the core pattern with typed message events, join/leave announcements,
and a message history log maintained by the mediator.
"""
from __future__ import annotations

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mediator_pattern import ChatRoom, User


def main() -> None:
    room = ChatRoom()

    users = [User(name, room) for name in ("Alice", "Bob", "Carol", "Dave")]
    for u in users:
        room.register(u)

    alice, bob, carol, dave = users

    print("\n=== Group conversation ===")
    alice.send("Good morning team!")
    bob.send("Morning Alice!")

    print("\n=== Private messages ===")
    carol.send_private("Dave", "Did you review the PR?")
    dave.send_private("Carol", "Yes, LGTM!")

    print("\n=== After Carol leaves ===")
    room.unregister(carol)
    alice.send("Where did Carol go?")

    print("\n=== Message counts ===")
    for u in users:
        print(f"  {u.name} inbox: {len(u.inbox)} messages")


if __name__ == "__main__":
    main()
