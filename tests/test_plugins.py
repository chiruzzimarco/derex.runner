from itertools import permutations

import pytest


def test_registry_exception():
    from derex.runner.plugins import Registry

    registry = Registry()
    registry.add("one", "one", "badlocation")

    with pytest.raises(ValueError):
        registry.add("one", "one", "badlocation")

    with pytest.raises(ValueError):
        registry.deregister("doesnotexist")


def test_registry_basic():
    from derex.runner.plugins import Registry

    registry = Registry()
    registry.add("last", "I should be last", "_end")
    registry.add("first", "I should be first", "_begin")
    registry.add(
        "in-between-1", "I should be the first in between first and last", ">first"
    )
    registry.add(
        "in-between-2", "I should be the second in between first and last", "<last"
    )

    assert registry["last"] == "I should be last"
    assert registry[-1] == "I should be last"
    assert registry["first"] == "I should be first"
    assert registry[0] == "I should be first"

    # Now move the last to the beginning, just to prove we can
    registry.add("last", "I should be last", "_begin")
    assert registry[0] == "I should be last"


def test_registry_add_list():
    from derex.runner.plugins import Registry

    # TODO: adding a third elemnt in between begin and end makes this not
    # work anymore. It's good enough for what we're using it (allowing users
    # to hint where they want their options) but can be greatly improved.
    to_add = [
        ("last", "I should be last", "_end"),
        ("first", "I should be first", "_begin"),
        ("in-between-1", "I should be the first in between first and last", ">first"),
        ("in-between-2", "I should be the second in between first and last", "<last"),
    ]

    for variant in permutations(to_add):
        registry = Registry()
        registry.add_list(variant)
        assert tuple(registry) == (
            "I should be first",
            "I should be the first in between first and last",
            "I should be the second in between first and last",
            "I should be last",
        )


def test_registry_add_list_impossible():
    from derex.runner.plugins import Registry

    to_add = [
        ("zero", "zero", "_begin"),
        ("one", "one", "<two"),
        ("two", "two", "<one"),
    ]

    registry = Registry()
    with pytest.raises(ValueError):
        registry.add_list(to_add)
