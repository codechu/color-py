"""GTK CSS adapter tests — emits text only, no GTK runtime needed."""

from __future__ import annotations

from codechu_color import RISK, Palette, to_gtk_css


def test_emits_class_per_color() -> None:
    css = to_gtk_css(RISK, prefix="risk-")
    assert ".risk-low { color: #1a7f37; }" in css
    assert ".risk-medium { color: #9a6700; }" in css
    assert ".risk-high { color: #cf222e; }" in css


def test_custom_prefix() -> None:
    css = to_gtk_css(RISK, prefix="severity-")
    assert ".severity-low" in css
    assert ".risk-low" not in css


def test_empty_palette_emits_empty_string() -> None:
    assert to_gtk_css(Palette()) == ""
