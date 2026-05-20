"""Color space conversions and WCAG helpers — stdlib only."""

from __future__ import annotations


def hex_to_rgb(hex_str: str) -> tuple[int, int, int]:
    """Parse ``#rgb`` or ``#rrggbb`` (case-insensitive, ``#`` optional)."""
    s = hex_str.strip().lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) != 6:
        raise ValueError(f"invalid hex color: {hex_str!r}")
    try:
        r = int(s[0:2], 16)
        g = int(s[2:4], 16)
        b = int(s[4:6], 16)
    except ValueError as exc:
        raise ValueError(f"invalid hex color: {hex_str!r}") from exc
    return (r, g, b)


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Render ``(r, g, b)`` (0-255) as lowercase ``#rrggbb``."""
    for v in (r, g, b):
        if not 0 <= v <= 255:
            raise ValueError(f"rgb component out of range: {(r, g, b)}")
    return f"#{r:02x}{g:02x}{b:02x}"


def rgb_to_hsl(r: int, g: int, b: int) -> tuple[float, float, float]:
    """Convert ``(r, g, b)`` (0-255) to HSL.

    Returns ``(h, s, l)`` where ``h`` is degrees in ``[0, 360)``,
    ``s`` and ``l`` are floats in ``[0, 1]``.
    """
    rf, gf, bf = r / 255.0, g / 255.0, b / 255.0
    mx = max(rf, gf, bf)
    mn = min(rf, gf, bf)
    light = (mx + mn) / 2.0
    if mx == mn:
        return (0.0, 0.0, light)
    d = mx - mn
    sat = d / (2.0 - mx - mn) if light > 0.5 else d / (mx + mn)
    if mx == rf:
        h = ((gf - bf) / d) % 6.0
    elif mx == gf:
        h = (bf - rf) / d + 2.0
    else:
        h = (rf - gf) / d + 4.0
    return (h * 60.0, sat, light)


def hsl_to_rgb(h: float, s: float, light: float) -> tuple[int, int, int]:
    """Convert HSL (``h`` degrees, ``s``/``l`` 0-1) to ``(r, g, b)`` 0-255."""
    if s == 0:
        v = round(light * 255)
        return (v, v, v)
    q = light + s - light * s if light < 0.5 else light + s - light * s
    # Standard formula (see CSS Color Module):
    q = light * (1 + s) if light < 0.5 else light + s - light * s
    p = 2 * light - q
    hk = (h % 360.0) / 360.0

    def _hue_to_channel(t: float) -> float:
        if t < 0:
            t += 1
        if t > 1:
            t -= 1
        if t < 1 / 6:
            return p + (q - p) * 6 * t
        if t < 1 / 2:
            return q
        if t < 2 / 3:
            return p + (q - p) * (2 / 3 - t) * 6
        return p

    r = _hue_to_channel(hk + 1 / 3)
    g = _hue_to_channel(hk)
    b = _hue_to_channel(hk - 1 / 3)
    return (round(r * 255), round(g * 255), round(b * 255))


def _linearize(channel_8bit: int) -> float:
    c = channel_8bit / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(rgb: tuple[int, int, int]) -> float:
    """WCAG 2.x relative luminance of an ``(r, g, b)`` triple (sRGB)."""
    r, g, b = rgb
    return 0.2126 * _linearize(r) + 0.7152 * _linearize(g) + 0.0722 * _linearize(b)


def contrast_ratio(rgb1: tuple[int, int, int], rgb2: tuple[int, int, int]) -> float:
    """WCAG contrast ratio between two colors (returns a value in ``[1, 21]``)."""
    l1 = relative_luminance(rgb1)
    l2 = relative_luminance(rgb2)
    lighter, darker = (l1, l2) if l1 >= l2 else (l2, l1)
    return (lighter + 0.05) / (darker + 0.05)


def pick_text_color(bg_rgb: tuple[int, int, int]) -> tuple[int, int, int]:
    """Return black or white — whichever has higher contrast against ``bg_rgb``."""
    white = (255, 255, 255)
    black = (0, 0, 0)
    return white if contrast_ratio(bg_rgb, white) >= contrast_ratio(bg_rgb, black) else black
