"""Color-space conversion + WCAG tests."""

from __future__ import annotations

import pytest

from codechu_color import (
    contrast_ratio,
    hex_to_rgb,
    hsl_to_rgb,
    pick_text_color,
    relative_luminance,
    rgb_to_hex,
    rgb_to_hsl,
)


class TestHexRgb:
    def test_round_trip_lowercase(self) -> None:
        assert rgb_to_hex(*hex_to_rgb("#1a7f37")) == "#1a7f37"

    def test_round_trip_uppercase(self) -> None:
        assert rgb_to_hex(*hex_to_rgb("#FF00AA")) == "#ff00aa"

    def test_three_digit_short_form(self) -> None:
        assert hex_to_rgb("#f0a") == (0xFF, 0x00, 0xAA)

    def test_no_leading_hash(self) -> None:
        assert hex_to_rgb("1a7f37") == (26, 127, 55)

    def test_invalid_length_raises(self) -> None:
        with pytest.raises(ValueError):
            hex_to_rgb("#12345")

    def test_invalid_chars_raises(self) -> None:
        with pytest.raises(ValueError):
            hex_to_rgb("#zzzzzz")

    def test_rgb_out_of_range_raises(self) -> None:
        with pytest.raises(ValueError):
            rgb_to_hex(256, 0, 0)


class TestHsl:
    def test_red_round_trip(self) -> None:
        h, s, light = rgb_to_hsl(255, 0, 0)
        assert h == 0.0
        assert s == pytest.approx(1.0)
        assert light == pytest.approx(0.5)
        assert hsl_to_rgb(h, s, light) == (255, 0, 0)

    def test_white_is_achromatic(self) -> None:
        h, s, light = rgb_to_hsl(255, 255, 255)
        assert s == 0.0
        assert light == pytest.approx(1.0)
        assert hsl_to_rgb(h, s, light) == (255, 255, 255)

    def test_black_is_achromatic(self) -> None:
        assert rgb_to_hsl(0, 0, 0) == (0.0, 0.0, 0.0)
        assert hsl_to_rgb(0, 0, 0) == (0, 0, 0)

    def test_green_round_trip(self) -> None:
        h, s, light = rgb_to_hsl(0, 255, 0)
        assert h == pytest.approx(120.0)
        assert hsl_to_rgb(h, s, light) == (0, 255, 0)

    def test_blue_round_trip(self) -> None:
        h, s, light = rgb_to_hsl(0, 0, 255)
        assert h == pytest.approx(240.0)
        assert hsl_to_rgb(h, s, light) == (0, 0, 255)


class TestWcag:
    def test_white_luminance_is_one(self) -> None:
        assert relative_luminance((255, 255, 255)) == pytest.approx(1.0)

    def test_black_luminance_is_zero(self) -> None:
        assert relative_luminance((0, 0, 0)) == pytest.approx(0.0)

    def test_white_black_contrast_is_21(self) -> None:
        # WCAG max contrast: black on white = 21:1
        assert contrast_ratio((255, 255, 255), (0, 0, 0)) == pytest.approx(21.0)

    def test_same_color_contrast_is_1(self) -> None:
        assert contrast_ratio((128, 128, 128), (128, 128, 128)) == pytest.approx(1.0)

    def test_contrast_is_symmetric(self) -> None:
        assert contrast_ratio((30, 80, 200), (220, 220, 220)) == pytest.approx(
            contrast_ratio((220, 220, 220), (30, 80, 200))
        )

    def test_pick_text_white_on_dark(self) -> None:
        assert pick_text_color((10, 10, 10)) == (255, 255, 255)

    def test_pick_text_black_on_light(self) -> None:
        assert pick_text_color((240, 240, 240)) == (0, 0, 0)

    def test_pick_text_known_brand_blue(self) -> None:
        # GitHub primary blue → white text recommended
        assert pick_text_color((9, 105, 218)) == (255, 255, 255)
