"""pytest tests for proxy pattern."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from proxy import CachingProxy, ProtectionProxy, RealService, VirtualProxy


class TestVirtualProxy:
    def test_not_loaded_before_first_call(self) -> None:
        vp = VirtualProxy()
        assert not vp.loaded

    def test_loaded_after_first_call(self) -> None:
        vp = VirtualProxy()
        vp.request("test")
        assert vp.loaded

    def test_lazy_load_happens_exactly_once(self) -> None:
        vp = VirtualProxy()
        for _ in range(5):
            vp.request("q")
        assert vp.load_count == 1

    def test_delegates_to_real_service(self) -> None:
        vp = VirtualProxy()
        result = vp.request("hello")
        assert "hello" in result

    def test_result_matches_real_service(self) -> None:
        vp = VirtualProxy()
        real = RealService()
        assert vp.request("xyz") == real.request("xyz")


class TestProtectionProxy:
    def setup_method(self) -> None:
        self.real = RealService()
        self.proxy = ProtectionProxy(self.real, {"alice", "bob"})

    def test_allowed_user_can_access(self) -> None:
        self.proxy.set_user("alice")
        result = self.proxy.request("data")
        assert "data" in result

    def test_denied_user_raises_permission_error(self) -> None:
        self.proxy.set_user("eve")
        with pytest.raises(PermissionError):
            self.proxy.request("data")

    def test_delegates_to_real_service(self) -> None:
        self.proxy.set_user("bob")
        assert self.proxy.request("q") == self.real.request("q")

    def test_empty_allowed_set_blocks_all(self) -> None:
        proxy = ProtectionProxy(self.real, set())
        proxy.set_user("alice")
        with pytest.raises(PermissionError):
            proxy.request("data")


class TestCachingProxy:
    def setup_method(self) -> None:
        self.real = RealService()
        self.proxy = CachingProxy(self.real)

    def test_first_call_is_a_miss(self) -> None:
        self.proxy.request("q1")
        assert self.proxy.miss_count == 1
        assert self.proxy.hit_count == 0

    def test_second_same_call_is_a_hit(self) -> None:
        self.proxy.request("q1")
        self.proxy.request("q1")
        assert self.proxy.hit_count == 1

    def test_result_consistent_with_cache(self) -> None:
        r1 = self.proxy.request("q2")
        r2 = self.proxy.request("q2")
        assert r1 == r2

    def test_different_queries_both_miss_initially(self) -> None:
        self.proxy.request("a")
        self.proxy.request("b")
        assert self.proxy.miss_count == 2
        assert self.proxy.hit_count == 0

    def test_invalidate_forces_re_fetch(self) -> None:
        self.proxy.request("q3")
        self.proxy.invalidate("q3")
        self.proxy.request("q3")
        assert self.proxy.miss_count == 2

    def test_delegates_to_real_service(self) -> None:
        assert self.proxy.request("x") == self.real.request("x")
