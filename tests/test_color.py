"""``Color`` dataclass tests."""

from __future__ import annotations

import pytest

from codechu_color import Color


class TestColorFactories:
    def test_from_hex_derives_rgb(self) -> None:
        c = Color.from_hex("#1a7f37", name="low")
        assert c.rgb == (26, 127, 55)
        assert c.hex == "#1a7f37"
        assert c.name == "low"

    def test_from_rgb_derives_hex(self) -> None:
        c = Color.from_rgb(26, 127, 55, name="low")
        assert c.hex == "#1a7f37"

    def test_from_ansi_derives_rgb_and_hex(self) -> None:
        c = Color.from_ansi(32, name="green")
        assert c.rgb == (0, 170, 0)
        assert c.hex == "#00aa00"
        assert c.ansi_code == 32

    def test_from_ansi_invalid_code_raises(self) -> None:
        with pytest.raises(ValueError):
            Color.from_ansi(123)


class TestColorAnsiEscapes:
    def test_fg_escape_format(self) -> None:
        c = Color.from_ansi(31)
        assert c.ansi_fg == "\x1b[31m"

    def test_bg_escape_is_fg_plus_10(self) -> None:
        c = Color.from_ansi(31)
        assert c.ansi_bg == "\x1b[41m"

    def test_nearest_ansi_for_dark_green(self) -> None:
        # GitHub low-risk green (#1a7f37) is closer to ANSI green (32) than red.
        c = Color.from_hex("#1a7f37")
        assert c.ansi_code == 32


class TestColorAlpha:
    def test_default_alpha_is_one(self) -> None:
        c = Color.from_rgb(10, 20, 30)
        assert c.rgba == (10, 20, 30, 1.0)

    def test_custom_alpha_in_rgba(self) -> None:
        c = Color.from_hex("#102030", alpha=0.5)
        assert c.rgba == (16, 32, 48, 0.5)


class TestColorImmutability:
    def test_color_is_frozen(self) -> None:
        c = Color.from_hex("#000000")
        with pytest.raises(Exception):
            c.name = "changed"  # type: ignore[misc]
