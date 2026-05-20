"""``Palette`` collection tests."""

from __future__ import annotations

import pytest

from codechu_color import Color, Palette


def _pal_ab() -> Palette:
    return Palette(
        {
            "a": Color.from_hex("#ff0000", name="a"),
            "b": Color.from_hex("#00ff00", name="b"),
        }
    )


class TestAccess:
    def test_attribute_access(self) -> None:
        pal = _pal_ab()
        assert pal.a.hex == "#ff0000"
        assert pal.b.hex == "#00ff00"

    def test_item_access(self) -> None:
        pal = _pal_ab()
        assert pal["a"].hex == "#ff0000"

    def test_missing_attribute_raises(self) -> None:
        pal = _pal_ab()
        with pytest.raises(AttributeError):
            _ = pal.nonexistent

    def test_contains_and_len(self) -> None:
        pal = _pal_ab()
        assert "a" in pal
        assert "z" not in pal
        assert len(pal) == 2

    def test_iter_yields_keys(self) -> None:
        pal = _pal_ab()
        assert sorted(pal) == ["a", "b"]


class TestMerge:
    def test_merge_overlays_keys(self) -> None:
        base = _pal_ab()
        overlay = Palette({"b": Color.from_hex("#0000ff", name="b")})
        merged = base.merge(overlay)
        assert merged.a.hex == "#ff0000"  # untouched
        assert merged.b.hex == "#0000ff"  # overridden
        # base is unchanged
        assert base.b.hex == "#00ff00"

    def test_merge_adds_new_keys(self) -> None:
        base = _pal_ab()
        merged = base.merge(Palette({"c": Color.from_hex("#abcdef")}))
        assert merged.c.hex == "#abcdef"
        assert len(merged) == 3


class TestToDict:
    def test_to_dict_is_flat_hex_mapping(self) -> None:
        pal = _pal_ab()
        assert pal.to_dict() == {"a": "#ff0000", "b": "#00ff00"}

    def test_empty_palette(self) -> None:
        pal = Palette()
        assert pal.to_dict() == {}
        assert len(pal) == 0
