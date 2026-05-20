"""Built-in palette + color-blind variant tests."""

from __future__ import annotations

import pytest

from codechu_color import (
    MATERIAL,
    RISK,
    SOLARIZED_DARK,
    SOLARIZED_LIGHT,
    TERMINAL,
    palette_for,
)


class TestBuiltins:
    def test_risk_has_three_levels(self) -> None:
        assert set(RISK.keys()) == {"low", "medium", "high"}

    def test_risk_low_is_green(self) -> None:
        # GitHub success green
        assert RISK.low.hex == "#1a7f37"

    def test_risk_high_is_red(self) -> None:
        assert RISK.high.hex == "#cf222e"

    def test_terminal_has_eight_basic_colors(self) -> None:
        assert len(TERMINAL) == 8
        assert "red" in TERMINAL
        assert "white" in TERMINAL

    def test_material_includes_blue_500(self) -> None:
        assert MATERIAL.blue.hex == "#2196f3"

    def test_solarized_light_base3(self) -> None:
        assert SOLARIZED_LIGHT.base3.hex == "#fdf6e3"

    def test_solarized_dark_has_same_accent_ramp(self) -> None:
        # Accent hexes are identical between light and dark variants.
        assert SOLARIZED_DARK.blue.hex == SOLARIZED_LIGHT.blue.hex


class TestPaletteFor:
    def test_default_returns_default_risk(self) -> None:
        assert palette_for("risk").low.hex == RISK.low.hex

    def test_protanopia_changes_high_color(self) -> None:
        prot = palette_for("risk", profile="protanopia")
        assert prot.high.hex != RISK.high.hex

    def test_deuteranopia_changes_low_color(self) -> None:
        deut = palette_for("risk", profile="deuteranopia")
        assert deut.low.hex != RISK.low.hex

    def test_tritanopia_changes_medium_color(self) -> None:
        trit = palette_for("risk", profile="tritanopia")
        assert trit.medium.hex != RISK.medium.hex

    def test_all_three_levels_present_in_every_profile(self) -> None:
        for profile in ("default", "protanopia", "deuteranopia", "tritanopia"):
            pal = palette_for("risk", profile=profile)
            assert set(pal.keys()) == {"low", "medium", "high"}

    def test_non_risk_palette_ignores_vision_profile(self) -> None:
        # Material doesn't have variants → returns default for any known profile.
        assert palette_for("material", profile="protanopia").blue.hex == MATERIAL.blue.hex

    def test_unknown_palette_raises(self) -> None:
        with pytest.raises(ValueError):
            palette_for("nope")

    def test_unknown_profile_raises(self) -> None:
        with pytest.raises(ValueError):
            palette_for("risk", profile="bogus")
