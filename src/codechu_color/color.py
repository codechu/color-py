"""``Color`` — a single color stored in multiple representations."""

from __future__ import annotations

from dataclasses import dataclass, field

from .convert import hex_to_rgb, rgb_to_hex

# ANSI 8-color base (foreground codes 30-37, background 40-47).
# These are the "standard" terminal palette approximations.
_ANSI_BASE: dict[int, tuple[int, int, int]] = {
    30: (0, 0, 0),
    31: (170, 0, 0),
    32: (0, 170, 0),
    33: (170, 85, 0),
    34: (0, 0, 170),
    35: (170, 0, 170),
    36: (0, 170, 170),
    37: (170, 170, 170),
    90: (85, 85, 85),
    91: (255, 85, 85),
    92: (85, 255, 85),
    93: (255, 255, 85),
    94: (85, 85, 255),
    95: (255, 85, 255),
    96: (85, 255, 255),
    97: (255, 255, 255),
}


def _nearest_ansi_fg(rgb: tuple[int, int, int]) -> int:
    """Pick the foreground ANSI code whose base RGB is closest (Euclidean)."""
    r, g, b = rgb
    best_code = 37
    best_dist = float("inf")
    for code, (br, bg, bb) in _ANSI_BASE.items():
        d = (r - br) ** 2 + (g - bg) ** 2 + (b - bb) ** 2
        if d < best_dist:
            best_dist = d
            best_code = code
    return best_code


@dataclass(frozen=True)
class Color:
    """A single color, accessible in ANSI / hex / RGB / RGBA forms.

    Construct via the factory methods :meth:`from_hex`, :meth:`from_rgb`,
    or :meth:`from_ansi`; the missing representations are derived
    automatically.
    """

    name: str = ""
    rgb: tuple[int, int, int] = (0, 0, 0)
    alpha: float = 1.0
    ansi_code: int = 37
    # Derived (computed in __post_init__):
    hex: str = field(init=False)
    rgba: tuple[int, int, int, float] = field(init=False)
    ansi_fg: str = field(init=False)
    ansi_bg: str = field(init=False)

    def __post_init__(self) -> None:
        # frozen=True → use object.__setattr__
        object.__setattr__(self, "hex", rgb_to_hex(*self.rgb))
        object.__setattr__(self, "rgba", (*self.rgb, self.alpha))
        object.__setattr__(self, "ansi_fg", f"\x1b[{self.ansi_code}m")
        bg_code = self.ansi_code + 10 if self.ansi_code < 90 else self.ansi_code + 10
        object.__setattr__(self, "ansi_bg", f"\x1b[{bg_code}m")

    # --- factories -----------------------------------------------------

    @classmethod
    def from_hex(cls, hex_str: str, *, name: str = "", alpha: float = 1.0) -> Color:
        rgb = hex_to_rgb(hex_str)
        return cls(name=name, rgb=rgb, alpha=alpha, ansi_code=_nearest_ansi_fg(rgb))

    @classmethod
    def from_rgb(cls, r: int, g: int, b: int, *, name: str = "", alpha: float = 1.0) -> Color:
        rgb = (r, g, b)
        return cls(name=name, rgb=rgb, alpha=alpha, ansi_code=_nearest_ansi_fg(rgb))

    @classmethod
    def from_ansi(cls, code: int, *, name: str = "") -> Color:
        if code not in _ANSI_BASE:
            raise ValueError(f"unsupported ANSI code: {code}")
        return cls(name=name, rgb=_ANSI_BASE[code], alpha=1.0, ansi_code=code)
