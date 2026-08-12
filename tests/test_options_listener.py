#!/usr/bin/env python3
"""Regression guard: the integration must never reload on OAuth token writes.

Home Assistant fires config-entry update listeners on ANY entry change,
including the hourly OAuth token write, so an unconditional ``async_reload()``
in that listener rebuilt this integration ~24x/day. Core owns reloading now:
``WhoopOptionsFlowHandler`` subclasses ``OptionsFlowWithReload``, which reloads
only when the options actually changed. The two must never coexist - core
raises ``ValueError`` if both are present.

No custom reload logic is left to exercise, so these are structural assertions
parsed from the source with ``ast`` - no Home Assistant, no pytest, no
stubbing, and they cannot pass vacuously::

    python3 tests/test_options_listener.py
"""

from __future__ import annotations

import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
INIT_PY = REPO_ROOT / "custom_components" / "whoop" / "__init__.py"
CONFIG_FLOW_PY = REPO_ROOT / "custom_components" / "whoop" / "config_flow.py"


def _parse(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def _called_attrs(node: ast.AST) -> set[str]:
    """Every attribute name invoked as a call beneath `node` (e.g. `x.foo()`)."""
    return {
        child.func.attr
        for child in ast.walk(node)
        if isinstance(child, ast.Call) and isinstance(child.func, ast.Attribute)
    }


def _find_function(tree: ast.Module, name: str) -> ast.AsyncFunctionDef | None:
    for node in ast.walk(tree):
        if isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef)) and node.name == name:
            return node  # type: ignore[return-value]
    return None


def _find_class(tree: ast.Module, name: str) -> ast.ClassDef | None:
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == name:
            return node
    return None


def _base_names(cls: ast.ClassDef) -> set[str]:
    names = set()
    for base in cls.bases:
        if isinstance(base, ast.Attribute):
            names.add(base.attr)
        elif isinstance(base, ast.Name):
            names.add(base.id)
    return names


# --------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------
def test_no_config_entry_update_listener() -> None:
    """THE regression guard: no update listener anywhere in the integration.

    An update listener fires on the hourly OAuth token write, not just on
    options changes. Registering one reintroduces the ~24 reloads/day.
    """
    tree = _parse(INIT_PY)

    assert "add_update_listener" not in _called_attrs(tree), (
        "__init__.py registers a config entry update listener. HA fires those "
        "on every entry change, including the hourly OAuth token write, so the "
        "integration will reload ~24x/day again. Let OptionsFlowWithReload "
        "handle reloading instead."
    )


def test_no_unconditional_reload_helper() -> None:
    """The old listener callback must be gone, not merely unregistered."""
    tree = _parse(INIT_PY)

    assert _find_function(tree, "async_options_updated") is None, (
        "async_options_updated still exists. It was the update-listener "
        "callback that reloaded on every entry write; core now owns reloading."
    )

    setup = _find_function(tree, "async_setup_entry")
    assert setup is not None, "async_setup_entry disappeared"
    assert "async_reload" not in _called_attrs(setup), (
        "async_setup_entry calls async_reload; setup must not reload itself."
    )


def test_options_flow_uses_reloading_base() -> None:
    """Options changes must still reload - core does it via this base class."""
    cls = _find_class(_parse(CONFIG_FLOW_PY), "WhoopOptionsFlowHandler")
    assert cls is not None, "WhoopOptionsFlowHandler not found in config_flow.py"

    bases = _base_names(cls)
    assert "OptionsFlowWithReload" in bases, (
        "WhoopOptionsFlowHandler must subclass config_entries.OptionsFlowWithReload "
        f"so a genuine options change still reloads the entry; got bases {bases!r}. "
        "Plain OptionsFlow would silently stop applying options changes now that "
        "the update listener is gone."
    )


def test_setup_still_applies_duration_unit_overrides() -> None:
    """Setup owns the entity-registry unit rewrite now the listener is gone.

    The old listener called _apply_duration_unit_overrides before reloading. It
    is only correct to drop that because async_setup_entry runs it after the
    platforms are forwarded, and an options change now reloads via core.
    """
    setup = _find_function(_parse(INIT_PY), "async_setup_entry")
    assert setup is not None, "async_setup_entry disappeared"

    called = {
        child.func.id
        for child in ast.walk(setup)
        if isinstance(child, ast.Call) and isinstance(child.func, ast.Name)
    }
    assert "_apply_duration_unit_overrides" in called, (
        "async_setup_entry no longer applies the duration unit overrides. With "
        "the update listener removed, setup is the only place they get applied, "
        "so duration units would silently stop working after an options change."
    )


def main() -> int:
    tests = [
        test_no_config_entry_update_listener,
        test_no_unconditional_reload_helper,
        test_options_flow_uses_reloading_base,
        test_setup_still_applies_duration_unit_overrides,
    ]

    failures = 0
    for test in tests:
        try:
            test()
        except AssertionError as err:
            failures += 1
            print(f"FAIL  {test.__name__}\n      {err}")
        except Exception as err:  # noqa: BLE001
            failures += 1
            print(f"ERROR {test.__name__}\n      {type(err).__name__}: {err}")
        else:
            print(f"ok    {test.__name__}")

    print(f"\n{len(tests) - failures}/{len(tests)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
