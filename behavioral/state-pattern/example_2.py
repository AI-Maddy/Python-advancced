"""State Pattern — Example 2: Network Connection State Machine.

A network connection moves through: Disconnected → Connecting → Connected
→ Disconnected.  Each state handles connect(), send(), disconnect() differently.
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class ConnectionState(ABC):
    @abstractmethod
    def connect(self, conn: NetworkConnection) -> None: ...
    @abstractmethod
    def send(self, conn: NetworkConnection, data: str) -> None: ...
    @abstractmethod
    def disconnect(self, conn: NetworkConnection) -> None: ...

    def __repr__(self) -> str:
        return type(self).__name__


class DisconnectedState(ConnectionState):
    def connect(self, conn: NetworkConnection) -> None:
        print(f"  [{conn.host}] Initiating connection...")
        conn.state = ConnectingState()
        # Simulate immediate success for demo
        conn.state.connect(conn)

    def send(self, conn: NetworkConnection, data: str) -> None:
        print(f"  [{conn.host}] Cannot send — not connected.")

    def disconnect(self, conn: NetworkConnection) -> None:
        print(f"  [{conn.host}] Already disconnected.")


class ConnectingState(ConnectionState):
    def connect(self, conn: NetworkConnection) -> None:
        print(f"  [{conn.host}] Handshake complete. Connected!")
        conn.state = ConnectedState()

    def send(self, conn: NetworkConnection, data: str) -> None:
        print(f"  [{conn.host}] Still connecting, buffering: '{data}'")

    def disconnect(self, conn: NetworkConnection) -> None:
        print(f"  [{conn.host}] Aborting connection.")
        conn.state = DisconnectedState()


class ConnectedState(ConnectionState):
    def connect(self, conn: NetworkConnection) -> None:
        print(f"  [{conn.host}] Already connected.")

    def send(self, conn: NetworkConnection, data: str) -> None:
        print(f"  [{conn.host}] Sent: '{data}'")

    def disconnect(self, conn: NetworkConnection) -> None:
        print(f"  [{conn.host}] Closing connection.")
        conn.state = DisconnectedState()


class NetworkConnection:
    def __init__(self, host: str) -> None:
        self.host = host
        self.state: ConnectionState = DisconnectedState()

    def connect(self) -> None:
        self.state.connect(self)

    def send(self, data: str) -> None:
        self.state.send(self, data)

    def disconnect(self) -> None:
        self.state.disconnect(self)

    def __repr__(self) -> str:
        return f"NetworkConnection(host={self.host!r}, state={self.state!r})"


def main() -> None:
    conn = NetworkConnection("api.example.com")
    print(f"Initial: {conn}\n")

    conn.send("Hello")      # should fail — not connected
    conn.connect()
    conn.send("GET /users")
    conn.send("POST /data")
    conn.disconnect()
    conn.send("After disconnect")  # should fail


if __name__ == "__main__":
    main()
