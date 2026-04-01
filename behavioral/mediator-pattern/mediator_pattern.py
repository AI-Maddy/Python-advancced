"""Mediator Pattern — centralises communication between objects.

The Mediator pattern defines an object that encapsulates how a set of objects
interact.  It promotes loose coupling by keeping objects from referring to
each other explicitly, and lets you vary their interaction independently.

Python-specific notes:
- ABC + @abstractmethod enforces the ``notify(sender, event)`` interface.
- Colleagues hold a reference to the mediator, not to each other.
- ``dataclass`` is used for simple colleague objects.
- Avoids the "star topology" of direct object-to-object references.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# Abstract mediator
# ---------------------------------------------------------------------------

class Mediator(ABC):
    """Abstract mediator that routes messages between colleagues."""

    @abstractmethod
    def notify(self, sender: object, event: str, data: Any = None) -> None:
        """Route a notification from *sender*.

        Args:
            sender: The colleague that triggered the event.
            event:  Name of the event.
            data:   Optional payload.
        """


# ---------------------------------------------------------------------------
# Colleagues
# ---------------------------------------------------------------------------

@dataclass
class User:
    """A chat-room participant that communicates via the mediator.

    Attributes:
        name:     Display name.
        mediator: The chat room mediator.
        inbox:    Received messages.
    """
    name: str
    mediator: Mediator
    inbox: list[str] = field(default_factory=list)

    def send(self, message: str) -> None:
        """Broadcast *message* via the mediator."""
        print(f"  [{self.name}] sends: {message}")
        self.mediator.notify(self, "message", message)

    def send_private(self, recipient: str, message: str) -> None:
        """Send *message* privately to *recipient* via the mediator."""
        print(f"  [{self.name}] DM → {recipient}: {message}")
        self.mediator.notify(self, "private", {"to": recipient, "text": message})

    def receive(self, sender_name: str, message: str) -> None:
        """Receive an incoming *message* from *sender_name*."""
        entry = f"[{sender_name}]: {message}"
        self.inbox.append(entry)
        print(f"  [{self.name}] received: {entry}")


# ---------------------------------------------------------------------------
# Concrete mediator — ChatRoom
# ---------------------------------------------------------------------------

class ChatRoom(Mediator):
    """Mediator that routes messages between registered ``User`` colleagues.

    Attributes:
        _users: Mapping from username to ``User`` instance.
    """

    def __init__(self) -> None:
        self._users: dict[str, User] = {}

    def register(self, user: User) -> None:
        """Register *user* with the chat room.

        Args:
            user: The user to add.
        """
        self._users[user.name] = user
        print(f"  [ChatRoom] {user.name} joined")

    def unregister(self, user: User) -> None:
        """Remove *user* from the chat room."""
        self._users.pop(user.name, None)
        print(f"  [ChatRoom] {user.name} left")

    def notify(self, sender: object, event: str, data: Any = None) -> None:
        """Route *event* from *sender* to the appropriate recipients."""
        if not isinstance(sender, User):
            return

        if event == "message":
            # Broadcast to everyone except sender
            for name, user in self._users.items():
                if name != sender.name:
                    user.receive(sender.name, str(data))

        elif event == "private":
            if isinstance(data, dict):
                recipient_name = data.get("to")
                text = data.get("text", "")
                target = self._users.get(str(recipient_name))
                if target:
                    target.receive(sender.name, f"(private) {text}")
                else:
                    print(f"  [ChatRoom] User '{recipient_name}' not found")


# ---------------------------------------------------------------------------
# Client demonstration
# ---------------------------------------------------------------------------

def main() -> None:
    room = ChatRoom()

    alice = User("Alice", room)
    bob = User("Bob", room)
    carol = User("Carol", room)

    room.register(alice)
    room.register(bob)
    room.register(carol)

    print("\n--- Broadcast ---")
    alice.send("Hello everyone!")

    print("\n--- Private message ---")
    bob.send_private("Carol", "Are you coming to the meeting?")

    print("\n--- Bob leaves ---")
    room.unregister(bob)
    alice.send("Bob left the room")

    print("\n--- Inboxes ---")
    for user in (alice, bob, carol):
        print(f"  {user.name}: {user.inbox}")


if __name__ == "__main__":
    main()
