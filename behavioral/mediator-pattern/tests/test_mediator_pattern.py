"""Tests for the Mediator Pattern implementation."""
from __future__ import annotations

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from mediator_pattern import ChatRoom, Mediator, User


class TestChatRoom:
    def _make_room(self) -> tuple[ChatRoom, User, User, User]:
        room = ChatRoom()
        alice = User("Alice", room)
        bob = User("Bob", room)
        carol = User("Carol", room)
        for u in (alice, bob, carol):
            room.register(u)
        return room, alice, bob, carol

    def test_broadcast_reaches_others(self) -> None:
        _, alice, bob, carol = self._make_room()
        alice.send("Hello!")
        assert any("Hello!" in msg for msg in bob.inbox)
        assert any("Hello!" in msg for msg in carol.inbox)

    def test_sender_does_not_receive_own_broadcast(self) -> None:
        _, alice, bob, carol = self._make_room()
        alice.send("Hello!")
        assert not any("Hello!" in msg for msg in alice.inbox)

    def test_private_message_only_reaches_recipient(self) -> None:
        _, alice, bob, carol = self._make_room()
        alice.send_private("Bob", "Secret")
        assert any("Secret" in msg for msg in bob.inbox)
        assert not any("Secret" in msg for msg in carol.inbox)

    def test_private_message_not_in_senders_inbox(self) -> None:
        _, alice, bob, carol = self._make_room()
        alice.send_private("Bob", "Secret")
        assert not any("Secret" in msg for msg in alice.inbox)

    def test_unregistered_user_stops_receiving(self) -> None:
        room, alice, bob, carol = self._make_room()
        room.unregister(bob)
        alice.send("After Bob left")
        assert not any("After Bob left" in msg for msg in bob.inbox)
        assert any("After Bob left" in msg for msg in carol.inbox)

    def test_private_to_nonexistent_user_does_not_raise(self) -> None:
        _, alice, bob, carol = self._make_room()
        alice.send_private("Zara", "Hi")  # Zara not registered

    def test_components_decoupled(self) -> None:
        """Users should not hold references to each other."""
        room, alice, bob, carol = self._make_room()
        # Users communicate only via mediator — no direct references
        assert not hasattr(alice, "bob") and not hasattr(alice, "carol")

    def test_mediator_abc_not_instantiable(self) -> None:
        with pytest.raises(TypeError):
            Mediator()  # type: ignore[abstract]
