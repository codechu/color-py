"""Built-in palettes and color-blind-safe variants.

Risk palette hex values follow GitHub's accessibility-tuned semantic
colors (success/attention/danger). Color-blind variants use the
Bang & Wong (2011) palette — *Points of view: Color blindness*,
Nature Methods 8 (6): 441 — which is widely adopted for protanopia,
deuteranopia, and tritanopia safety.
"""

from __future__ import annotations

from .color import Color
from .palette import Palette

# --- Risk (semantic: low / medium / high) -----------------------------
# Default — GitHub's "success" / "attention" / "danger" foreground tones.
RISK = Palette(
    {
        "low": Color.from_hex("#1a7f37", name="low"),
        "medium": Color.from_hex("#9a6700", name="medium"),
        "high": Color.from_hex("#cf222e", name="high"),
    }
)

# --- Terminal (basic ANSI 8) ------------------------------------------
TERMINAL = Palette(
    {
        "black": Color.from_ansi(30, name="black"),
        "red": Color.from_ansi(31, name="red"),
        "green": Color.from_ansi(32, name="green"),
        "yellow": Color.from_ansi(33, name="yellow"),
        "blue": Color.from_ansi(34, name="blue"),
        "magenta": Color.from_ansi(35, name="magenta"),
        "cyan": Color.from_ansi(36, name="cyan"),
        "white": Color.from_ansi(37, name="white"),
    }
)

# --- Material Design Primary 500 tones --------------------------------
MATERIAL = Palette(
    {
        "red": Color.from_hex("#f44336", name="red"),
        "pink": Color.from_hex("#e91e63", name="pink"),
        "purple": Color.from_hex("#9c27b0", name="purple"),
        "deep_purple": Color.from_hex("#673ab7", name="deep_purple"),
        "indigo": Color.from_hex("#3f51b5", name="indigo"),
        "blue": Color.from_hex("#2196f3", name="blue"),
        "light_blue": Color.from_hex("#03a9f4", name="light_blue"),
        "cyan": Color.from_hex("#00bcd4", name="cyan"),
        "teal": Color.from_hex("#009688", name="teal"),
        "green": Color.from_hex("#4caf50", name="green"),
        "light_green": Color.from_hex("#8bc34a", name="light_green"),
        "lime": Color.from_hex("#cddc39", name="lime"),
        "yellow": Color.from_hex("#ffeb3b", name="yellow"),
        "amber": Color.from_hex("#ffc107", name="amber"),
        "orange": Color.from_hex("#ff9800", name="orange"),
        "deep_orange": Color.from_hex("#ff5722", name="deep_orange"),
        "brown": Color.from_hex("#795548", name="brown"),
        "grey": Color.from_hex("#9e9e9e", name="grey"),
        "blue_grey": Color.from_hex("#607d8b", name="blue_grey"),
    }
)

# --- Solarized (Ethan Schoonover) -------------------------------------
SOLARIZED_LIGHT = Palette(
    {
        "base03": Color.from_hex("#002b36", name="base03"),
        "base02": Color.from_hex("#073642", name="base02"),
        "base01": Color.from_hex("#586e75", name="base01"),
        "base00": Color.from_hex("#657b83", name="base00"),
        "base0": Color.from_hex("#839496", name="base0"),
        "base1": Color.from_hex("#93a1a1", name="base1"),
        "base2": Color.from_hex("#eee8d5", name="base2"),
        "base3": Color.from_hex("#fdf6e3", name="base3"),
        "yellow": Color.from_hex("#b58900", name="yellow"),
        "orange": Color.from_hex("#cb4b16", name="orange"),
        "red": Color.from_hex("#dc322f", name="red"),
        "magenta": Color.from_hex("#d33682", name="magenta"),
        "violet": Color.from_hex("#6c71c4", name="violet"),
        "blue": Color.from_hex("#268bd2", name="blue"),
        "cyan": Color.from_hex("#2aa198", name="cyan"),
        "green": Color.from_hex("#859900", name="green"),
    }
)

SOLARIZED_DARK = Palette(
    {
        # Same accent hexes; background/foreground roles swap on the
        # consumer side. The accent ramp is identical by design.
        **{k: v for k, v in SOLARIZED_LIGHT.items()},
    }
)

# --- Color-blind safe risk variants -----------------------------------
# Bang & Wong (2011) palette colors used here:
#   orange       #e69f00   blue           #0072b2
#   sky-blue     #56b4e9   vermilion      #d55e00
#   bluish-green #009e73   reddish-purple #cc79a7
#   yellow       #f0e442   black          #000000

_RISK_PROTANOPIA = Palette(
    {
        # Red is unreliable for protans → swap "high" to vermilion,
        # "medium" to orange, "low" to bluish-green.
        "low": Color.from_hex("#009e73", name="low"),
        "medium": Color.from_hex("#e69f00", name="medium"),
        "high": Color.from_hex("#d55e00", name="high"),
    }
)

_RISK_DEUTERANOPIA = Palette(
    {
        # Deutans confuse red/green; lean on blue vs orange vs vermilion.
        "low": Color.from_hex("#0072b2", name="low"),
        "medium": Color.from_hex("#e69f00", name="medium"),
        "high": Color.from_hex("#d55e00", name="high"),
    }
)

_RISK_TRITANOPIA = Palette(
    {
        # Tritans confuse blue/yellow; use reddish-purple, vermilion, sky-blue.
        "low": Color.from_hex("#56b4e9", name="low"),
        "medium": Color.from_hex("#cc79a7", name="medium"),
        "high": Color.from_hex("#d55e00", name="high"),
    }
)

_PALETTES: dict[str, dict[str, Palette]] = {
    "risk": {
        "default": RISK,
        "protanopia": _RISK_PROTANOPIA,
        "deuteranopia": _RISK_DEUTERANOPIA,
        "tritanopia": _RISK_TRITANOPIA,
    },
    "terminal": {"default": TERMINAL},
    "material": {"default": MATERIAL},
    "solarized_light": {"default": SOLARIZED_LIGHT},
    "solarized_dark": {"default": SOLARIZED_DARK},
}


def palette_for(name: str, profile: str = "default") -> Palette:
    """Return a built-in palette, optionally tuned for a vision profile.

    ``name`` is one of ``"risk"``, ``"terminal"``, ``"material"``,
    ``"solarized_light"``, ``"solarized_dark"``. ``profile`` is one of
    ``"default"``, ``"protanopia"``, ``"deuteranopia"``, ``"tritanopia"`` —
    only ``"risk"`` currently has non-default variants; other palettes
    return their default for any profile.
    """
    if name not in _PALETTES:
        raise ValueError(f"unknown palette: {name!r}")
    variants = _PALETTES[name]
    if profile in variants:
        return variants[profile]
    if profile in {"default", "protanopia", "deuteranopia", "tritanopia"}:
        return variants["default"]
    raise ValueError(f"unknown vision profile: {profile!r}")
