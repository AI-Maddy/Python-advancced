"""
Example 2 — Middleware stack.

HTTP request handlers are decorated with logging, auth, and rate-limiting
middleware, stacked in order.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Request:
    path: str
    method: str = "GET"
    headers: dict[str, str] | None = None

    def __post_init__(self) -> None:
        if self.headers is None:
            self.headers = {}


@dataclass
class Response:
    status: int
    body: str


class Handler(ABC):
    @abstractmethod
    def handle(self, request: Request) -> Response: ...


class RealHandler(Handler):
    def handle(self, request: Request) -> Response:
        return Response(200, f"OK: {request.path}")


class MiddlewareDecorator(Handler, ABC):
    def __init__(self, inner: Handler) -> None:
        self._inner = inner


class LoggingMiddleware(MiddlewareDecorator):
    def handle(self, request: Request) -> Response:
        print(f"[LOG] {request.method} {request.path}")
        response = self._inner.handle(request)
        print(f"[LOG] Response: {response.status}")
        return response


class AuthMiddleware(MiddlewareDecorator):
    def __init__(self, inner: Handler, token: str) -> None:
        super().__init__(inner)
        self._token = token

    def handle(self, request: Request) -> Response:
        auth = (request.headers or {}).get("Authorization", "")
        if auth != f"Bearer {self._token}":
            return Response(401, "Unauthorized")
        return self._inner.handle(request)


class RateLimitMiddleware(MiddlewareDecorator):
    def __init__(self, inner: Handler, limit: int) -> None:
        super().__init__(inner)
        self._limit = limit
        self._count = 0

    def handle(self, request: Request) -> Response:
        self._count += 1
        if self._count > self._limit:
            return Response(429, "Too Many Requests")
        return self._inner.handle(request)


def build_stack(token: str = "secret", limit: int = 5) -> Handler:
    handler: Handler = RealHandler()
    handler = AuthMiddleware(handler, token)
    handler = RateLimitMiddleware(handler, limit)
    handler = LoggingMiddleware(handler)
    return handler


def main() -> None:
    stack = build_stack(token="abc", limit=2)
    r1 = Request("/api/users", headers={"Authorization": "Bearer abc"})
    r2 = Request("/api/users", headers={"Authorization": "Bearer abc"})
    r3 = Request("/api/users", headers={"Authorization": "Bearer abc"})
    r_bad = Request("/api/users", headers={"Authorization": "Bearer wrong"})

    for req in (r1, r2, r3, r_bad):
        resp = stack.handle(req)
        print(f"  → {resp.status}: {resp.body}")


if __name__ == "__main__":
    main()
