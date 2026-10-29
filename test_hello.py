"""Tests for the :mod:`hello` module."""

from __future__ import annotations

import pytest

from hello import add


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (1, 2, 3),
        (0, 0, 0),
        (-1, 1, 0),
        (-3, -4, -7),
        (1000000, 2000000, 3000000),
    ],
)
def test_add(a: int, b: int, expected: int) -> None:
    """``add`` should return the arithmetic sum of its arguments."""
    assert add(a, b) == expected


def test_add_is_commutative() -> None:
    """``add(a, b)`` should equal ``add(b, a)``."""
    assert add(2, 5) == add(5, 2)
