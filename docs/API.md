# API Reference — codechu-color 0.1.0

Complete reference for every public symbol re-exported from the
`codechu_color` package. Pure stdlib, Python 3.10+, zero runtime
dependencies.

| Symbol                                          | Kind          | Module                       |
| ----------------------------------------------- | ------------- | ---------------------------- |
| [`__version__`](#__version__)                   | `str`         | `codechu_color`              |
| [`Color`](#color)                               | dataclass     | `codechu_color.color`        |
| [`Palette`](#palette)                           | class         | `codechu_color.palette`      |
| [`palette_for`](#palette_for)                   | function      | `codechu_color.palettes`     |
| [`RISK`, `TERMINAL`, `MATERIAL`, `SOLARIZED_LIGHT`, `SOLARIZED_DARK`](#built-in-palettes) | `Palette` | `codechu_color.palettes` |
| [`hex_to_rgb`](#hex_to_rgb) / [`rgb_to_hex`](#rgb_to_hex) | function | `codechu_color.convert` |
| [`rgb_to_hsl`](#rgb_to_hsl) / [`hsl_to_rgb`](#hsl_to_rgb) | function | `codechu_color.convert` |
| [`relative_luminance`](#relative_luminance)     | function      | `codechu_color.convert`      |
| [`contrast_ratio`](#contrast_ratio)             | function      | `codechu_color.convert`      |
| [`pick_text_color`](#pick_text_color)           | function      | `codechu_color.convert`      |
| [`to_gtk_css`](#to_gtk_css)                     | function      | `codechu_color.gtk`          |

---

## `__version__`

```python
__version__: str = "0.1.0"
```

---

## `Color`

```python
@dataclass(frozen=True)
class Color:
    name: str = ""
    rgb: tuple[int, int, int] = (0, 0, 0)
    alpha: float = 1.0
    ansi_code: int = 37
    # Derived (read-only):
    hex: str
    rgba: tuple[int, int, int, float]
    ansi_fg: str  # e.g. "\x1b[32m"
    ansi_bg: str  # e.g. "\x1b[42m"
```

A single color held simultaneously in ANSI / hex / RGB / RGBA forms.
Frozen dataclass — hashable, safe in `set`/`dict`. Derived fields
(`hex`, `rgba`, `ansi_fg`, `ansi_bg`) are computed in
`__post_init__`.

### Factories

| Method                                                          | Returns | Notes                                                                 |
| --------------------------------------------------------------- | ------- | --------------------------------------------------------------------- |
| `Color.from_hex(hex_str, *, name="", alpha=1.0)`                | `Color` | Accepts `"#1a7f37"` or `"1a7f37"`. ANSI code = nearest base-8 match.  |
| `Color.from_rgb(r, g, b, *, name="", alpha=1.0)`                | `Color` | Channels are 0-255 ints.                                              |
| `Color.from_ansi(code, *, name="")`                             | `Color` | `code` must be in the 8/16-color base set (30-37, 90-97).             |

### Example

```python
from codechu_color import Color
green = Color.from_hex("#1a7f37", name="low")
green.rgb       # (26, 127, 55)
green.hex       # "#1a7f37"
green.ansi_fg   # "\x1b[32m"
green.ansi_bg   # "\x1b[42m"
```

---

## `Palette`

```python
class Palette:
    def __init__(self, colors: dict[str, Color] | None = None) -> None: ...
    def __getitem__(self, key: str) -> Color: ...
    def __getattr__(self, name: str) -> Color: ...
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...
    def __contains__(self, key: object) -> bool: ...
    def keys(self) -> Iterator[str]: ...
    def values(self) -> Iterator[Color]: ...
    def items(self) -> Iterator[tuple[str, Color]]: ...
    def merge(self, other: Palette) -> Palette: ...
    def to_dict(self) -> dict[str, str]: ...
```

A named collection of `Color` instances with both mapping access
(`pal["low"]`) and attribute access (`pal.low`).

- `merge(other)` — returns a *new* palette with `other`'s keys
  overlaid on `self`. Neither operand is mutated.
- `to_dict()` — flat `{name: hex}` mapping, suitable for JSON dump
  or feeding into [`to_gtk_css`](#to_gtk_css).

```python
from codechu_color import Palette, Color
pal = Palette({"low": Color.from_hex("#1a7f37", name="low")})
pal.low.hex                                          # "#1a7f37"
pal.to_dict()                                        # {"low": "#1a7f37"}
```

`AttributeError` is raised for missing attribute access — never
`KeyError`.

---

## `palette_for`

```python
def palette_for(name: str, profile: str = "default") -> Palette: ...
```

Return a built-in palette, optionally tuned for a vision profile.

| Param     | Allowed values                                                                                        |
| --------- | ----------------------------------------------------------------------------------------------------- |
| `name`    | `"risk"`, `"terminal"`, `"material"`, `"solarized_light"`, `"solarized_dark"`                         |
| `profile` | `"default"`, `"protanopia"`, `"deuteranopia"`, `"tritanopia"`                                         |

Only `"risk"` currently ships color-blind safe variants (Bang & Wong
2011 — *Nature Methods* 8: 441). Other palettes return their default
for any profile.

```python
from codechu_color import palette_for
pal = palette_for("risk", profile="deuteranopia")
pal.high.hex   # "#d55e00" — vermilion, safe for red-green confusion
```

Unknown `name` → `ValueError("unknown palette: ...")`.
Unknown `profile` → `ValueError("unknown vision profile: ...")`.

---

## Built-in palettes

Module-level `Palette` constants — import directly when you don't
need a vision profile.

| Constant            | Keys                                                                                                                                                       |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `RISK`              | `low`, `medium`, `high` (GitHub semantic green / amber / red).                                                                                             |
| `TERMINAL`          | `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white` (basic ANSI 8).                                                                       |
| `MATERIAL`          | Material Design Primary 500 tones (`red`, `pink`, `purple`, `deep_purple`, `indigo`, `blue`, `light_blue`, `cyan`, `teal`, `green`, …).                    |
| `SOLARIZED_LIGHT`   | Full accent ramp (`yellow`, `orange`, `red`, `magenta`, `violet`, `blue`, `cyan`, `green`) + base tones.                                                    |
| `SOLARIZED_DARK`    | Same key set as `SOLARIZED_LIGHT`, tuned for dark backgrounds.                                                                                             |

```python
from codechu_color import RISK, MATERIAL
RISK.low.hex            # "#1a7f37"
MATERIAL.indigo.hex     # "#3f51b5"
```

---

## `hex_to_rgb`

```python
def hex_to_rgb(hex_str: str) -> tuple[int, int, int]: ...
```

Parse `"#rrggbb"` or `"rrggbb"` → `(r, g, b)`. Case-insensitive.
Raises `ValueError` for malformed input.

```python
hex_to_rgb("#1a7f37")   # (26, 127, 55)
hex_to_rgb("1a7f37")    # (26, 127, 55)
```

## `rgb_to_hex`

```python
def rgb_to_hex(r: int, g: int, b: int) -> str: ...
```

Format three 0-255 ints → `"#rrggbb"` (lowercase). Out-of-range
channels are *not* clamped — pass valid 0-255 values.

```python
rgb_to_hex(26, 127, 55)   # "#1a7f37"
```

## `rgb_to_hsl`

```python
def rgb_to_hsl(r: int, g: int, b: int) -> tuple[float, float, float]: ...
```

Convert sRGB → HSL. Returns `(h, s, l)` where `h ∈ [0, 360)`,
`s, l ∈ [0, 1]`.

## `hsl_to_rgb`

```python
def hsl_to_rgb(h: float, s: float, light: float) -> tuple[int, int, int]: ...
```

Inverse of `rgb_to_hsl`. Channels are rounded to nearest int and
clamped into `[0, 255]`.

---

## `relative_luminance`

```python
def relative_luminance(rgb: tuple[int, int, int]) -> float: ...
```

WCAG 2.1 §1.4.3 relative luminance (`Y`). Result in `[0.0, 1.0]`.

```python
relative_luminance((255, 255, 255))   # 1.0
relative_luminance((0, 0, 0))         # 0.0
```

## `contrast_ratio`

```python
def contrast_ratio(
    rgb1: tuple[int, int, int],
    rgb2: tuple[int, int, int],
) -> float: ...
```

WCAG 2.1 §1.4.3 contrast ratio. Result in `[1.0, 21.0]`. Order of
arguments does not matter.

| Use case                              | Minimum ratio |
| ------------------------------------- | ------------- |
| WCAG AA — normal text                 | 4.5           |
| WCAG AA — large text (≥ 18 pt)        | 3.0           |
| WCAG AAA — normal text                | 7.0           |
| WCAG AAA — large text                 | 4.5           |

```python
contrast_ratio((255, 255, 255), (0, 0, 0))   # 21.0
contrast_ratio((9, 105, 218), (255, 255, 255))  # ~4.65 (AA pass)
```

## `pick_text_color`

```python
def pick_text_color(bg_rgb: tuple[int, int, int]) -> tuple[int, int, int]: ...
```

Pick `(255, 255, 255)` (white) or `(0, 0, 0)` (black), whichever
gives the higher contrast against `bg_rgb`. Use for chip / badge /
status-pill text.

```python
pick_text_color((9, 105, 218))     # (255, 255, 255)
pick_text_color((255, 248, 220))   # (0, 0, 0)
```

---

## `to_gtk_css`

```python
def to_gtk_css(palette: Palette, prefix: str = "risk-") -> str: ...
```

Emit a CSS string with one class rule per color, suitable for
`Gtk.CssProvider.load_from_data()`. Each rule sets `color` (the
GTK-CSS foreground for the `Gtk.Widget`).

```python
from codechu_color import RISK, to_gtk_css
css = to_gtk_css(RISK, prefix="risk-")
# .risk-low { color: #1a7f37; }
# .risk-medium { color: #9a6700; }
# .risk-high { color: #cf222e; }
```

The output is deterministic (insertion order of the palette) so
golden-file tests are easy.

---

## Edge cases

- **`Color` equality**: frozen dataclass, structural equality on all
  init fields *plus* derived ones (because they participate in
  `__eq__`/`__hash__` until set via `__setattr__` after init —
  practically: two `Color`s built the same way compare equal).
- **`Palette` ordering**: iteration follows insertion order, like a
  plain `dict`. `to_dict()` preserves it.
- **Color-blind data source**: the non-default `"risk"` variants are
  derived from Bang & Wong, *Nature Methods* (2011) 8: 441.
