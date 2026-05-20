"""codechu-color — stdlib-only color palettes and format converters.

Public API:

- :class:`Color`           — single color in ANSI / hex / RGB / RGBA
- :class:`Palette`         — named collection with attribute access
- :func:`palette_for`      — built-in palette tuned for a vision profile
- Built-in palettes: :data:`RISK`, :data:`TERMINAL`, :data:`MATERIAL`,
  :data:`SOLARIZED_LIGHT`, :data:`SOLARIZED_DARK`
- Color-space helpers: :func:`hex_to_rgb`, :func:`rgb_to_hex`,
  :func:`rgb_to_hsl`, :func:`hsl_to_rgb`
- WCAG helpers: :func:`relative_luminance`, :func:`contrast_ratio`,
  :func:`pick_text_color`
- GTK adapter: :func:`to_gtk_css`
"""

from __future__ import annotations

from .color import Color
from .convert import (
    contrast_ratio,
    hex_to_rgb,
    hsl_to_rgb,
    pick_text_color,
    relative_luminance,
    rgb_to_hex,
    rgb_to_hsl,
)
from .gtk import to_gtk_css
from .palette import Palette
from .palettes import (
    MATERIAL,
    RISK,
    SOLARIZED_DARK,
    SOLARIZED_LIGHT,
    TERMINAL,
    palette_for,
)

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "Color",
    "Palette",
    "palette_for",
    "RISK",
    "TERMINAL",
    "MATERIAL",
    "SOLARIZED_LIGHT",
    "SOLARIZED_DARK",
    "hex_to_rgb",
    "rgb_to_hex",
    "rgb_to_hsl",
    "hsl_to_rgb",
    "relative_luminance",
    "contrast_ratio",
    "pick_text_color",
    "to_gtk_css",
]
