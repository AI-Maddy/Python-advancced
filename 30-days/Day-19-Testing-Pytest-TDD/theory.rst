Day 19 — Testing, Pytest & TDD
================================

pytest Fundamentals
--------------------

.. code-block:: python

    # Basic test function
    def test_add() -> None:
        assert add(1, 2) == 3

Fixtures
--------

.. code-block:: python

    import pytest

    @pytest.fixture
    def db() -> Database:
        d = Database(":memory:")
        d.init()
        yield d     # teardown happens after yield
        d.close()

    def test_query(db: Database) -> None:
        assert db.count() == 0

Place shared fixtures in ``conftest.py`` — auto-discovered by pytest.

Parametrize
-----------

.. code-block:: python

    @pytest.mark.parametrize("a,b,expected", [
        (1, 2, 3),
        (0, 0, 0),
        (-1, 1, 0),
    ])
    def test_add(a: int, b: int, expected: int) -> None:
        assert add(a, b) == expected

Useful Assertions
-----------------

.. code-block:: python

    with pytest.raises(ValueError, match="invalid"):
        parse("")

    with pytest.warns(DeprecationWarning):
        old_api()

    assert 0.1 + 0.2 == pytest.approx(0.3)

Mocking
-------

.. code-block:: python

    from unittest.mock import Mock, MagicMock, patch

    # Mock with return value
    m = Mock()
    m.fetch.return_value = {"data": 42}

    # Mock with side_effect (exception or callable)
    m.fetch.side_effect = ConnectionError("timeout")

    # Patch at the point of use (not where it is defined)
    with patch("mymodule.requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"ok": True}
        result = my_function()

TDD Cycle
---------

1. **Red** — write a failing test for the feature you want.
2. **Green** — write minimal code to make the test pass.
3. **Refactor** — improve code quality while keeping tests green.

Benefits: forces clear interface design before implementation.

Coverage
--------

.. code-block:: bash

    pip install pytest-cov
    pytest --cov=src --cov-report=term-missing

Hypothesis (Property-Based)
-----------------------------

.. code-block:: python

    from hypothesis import given, strategies as st

    @given(st.lists(st.integers()))
    def test_reverse_twice_is_identity(lst: list[int]) -> None:
        assert list(reversed(list(reversed(lst)))) == lst

Hypothesis generates hundreds of random inputs automatically,
including edge cases like empty lists, very large integers, etc.

Marks
-----

.. code-block:: python

    @pytest.mark.slow
    @pytest.mark.skip(reason="not implemented")
    @pytest.mark.xfail(reason="known bug #123")
    @pytest.mark.skipif(sys.platform == "win32", reason="unix only")
