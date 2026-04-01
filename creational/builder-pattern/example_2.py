"""
Example 2 — HTTP request builder.

Builds an immutable HttpRequest object step by step.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class HttpRequest:
    """Immutable HTTP request product."""
    method: str
    url: str
    headers: tuple[tuple[str, str], ...]
    body: str | None
    timeout_sec: int

    def __str__(self) -> str:
        lines = [f"{self.method} {self.url}"]
        for name, value in self.headers:
            lines.append(f"  {name}: {value}")
        if self.body:
            lines.append(f"  Body: {self.body[:60]}...")
        lines.append(f"  Timeout: {self.timeout_sec}s")
        return "\n".join(lines)


class HttpRequestBuilder:
    """Fluent builder for HttpRequest."""

    def __init__(self) -> None:
        self._method = "GET"
        self._url = ""
        self._headers: list[tuple[str, str]] = []
        self._body: str | None = None
        self._timeout = 30

    def method(self, method: str) -> HttpRequestBuilder:
        self._method = method.upper()
        return self

    def url(self, url: str) -> HttpRequestBuilder:
        self._url = url
        return self

    def header(self, name: str, value: str) -> HttpRequestBuilder:
        self._headers.append((name, value))
        return self

    def bearer_auth(self, token: str) -> HttpRequestBuilder:
        return self.header("Authorization", f"Bearer {token}")

    def json_body(self, body: str) -> HttpRequestBuilder:
        self._body = body
        return self.header("Content-Type", "application/json")

    def timeout(self, seconds: int) -> HttpRequestBuilder:
        self._timeout = seconds
        return self

    def build(self) -> HttpRequest:
        return HttpRequest(
            method=self._method,
            url=self._url,
            headers=tuple(self._headers),
            body=self._body,
            timeout_sec=self._timeout,
        )


def main() -> None:
    get_request = (
        HttpRequestBuilder()
        .method("GET")
        .url("https://api.example.com/users")
        .bearer_auth("my-token-xyz")
        .timeout(10)
        .build()
    )
    print("GET Request:")
    print(get_request)

    post_request = (
        HttpRequestBuilder()
        .method("POST")
        .url("https://api.example.com/users")
        .bearer_auth("my-token-xyz")
        .json_body('{"name": "Alice", "email": "alice@example.com"}')
        .build()
    )
    print("\nPOST Request:")
    print(post_request)


if __name__ == "__main__":
    main()
