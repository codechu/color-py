"""GTK CSS adapter — emits class definitions from a :class:`Palette`.

This module is import-safe without GTK installed; it only produces a
CSS text string. Consumers that load it into a GTK ``CssProvider`` do
so on their side.
"""

from __future__ import annotations

from .palette import Palette


def to_gtk_css(palette: Palette, prefix: str = "risk-") -> str:
    """Render ``palette`` as GTK CSS class definitions.

    For each ``name → color`` in the palette, emits::

        .<prefix><name> { color: <hex>; }

    Example: ``to_gtk_css(RISK, prefix="risk-")`` produces classes
    ``.risk-low``, ``.risk-medium``, ``.risk-high``.
    """
    lines = [f".{prefix}{name} {{ color: {color.hex}; }}" for name, color in palette.items()]
    return "\n".join(lines) + ("\n" if lines else "")
