"""``Palette`` — a named collection of :class:`Color` instances."""

from __future__ import annotations

from typing import Iterator

from .color import Color


class Palette:
    """A named collection of colors with attribute access.

    Colors are accessed by their key, either via ``pal["low"]`` or
    ``pal.low``. Use :meth:`merge` to overlay another palette's keys
    and :meth:`to_dict` for a flat ``name → hex`` mapping suitable for
    GTK CSS or JSON export.
    """

    __slots__ = ("_colors",)

    def __init__(self, colors: dict[str, Color] | None = None) -> None:
        self._colors: dict[str, Color] = dict(colors or {})

    # --- mapping-ish ---------------------------------------------------

    def __getitem__(self, key: str) -> Color:
        return self._colors[key]

    def __contains__(self, key: object) -> bool:
        return key in self._colors

    def __iter__(self) -> Iterator[str]:
        return iter(self._colors)

    def __len__(self) -> int:
        return len(self._colors)

    def keys(self) -> Iterator[str]:
        return iter(self._colors.keys())

    def values(self) -> Iterator[Color]:
        return iter(self._colors.values())

    def items(self) -> Iterator[tuple[str, Color]]:
        return iter(self._colors.items())

    # --- attribute access ---------------------------------------------

    def __getattr__(self, name: str) -> Color:
        # __getattr__ only fires on missing attrs; __slots__ keeps that true.
        try:
            return self._colors[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    # --- combinators --------------------------------------------------

    def merge(self, other: Palette) -> Palette:
        """Return a new palette with ``other``'s keys overlaid on this one."""
        combined = dict(self._colors)
        combined.update(other._colors)
        return Palette(combined)

    def to_dict(self) -> dict[str, str]:
        """Flat ``{name: hex}`` mapping — useful for GTK CSS / JSON export."""
        return {key: color.hex for key, color in self._colors.items()}

    def __repr__(self) -> str:
        keys = ", ".join(self._colors.keys())
        return f"Palette({{{keys}}})"
