# codechu-color

Stdlib-only color palettes and format converters for Python 3.10+.
Zero runtime dependencies.

Solves the cross-surface palette drift problem: CLI tools work in
ANSI escapes, GTK apps work in hex / CSS, JSON exports want flat
dicts. `codechu-color` keeps one source of truth and derives the rest.

## Install

```bash
pip install codechu-color
```

## Quick start

```python
from codechu_color import Color, Palette, RISK, palette_for, to_gtk_css

# Single color in every form
green = Color.from_hex("#1a7f37", name="low")
green.rgb       # (26, 127, 55)
green.ansi_fg   # "\x1b[32m"
green.ansi_bg   # "\x1b[42m"

# Built-in semantic palette (GitHub accessibility-tuned)
RISK.low.hex    # "#1a7f37"
RISK.high.hex   # "#cf222e"

# Color-blind safe variants (Bang & Wong 2011)
pal = palette_for("risk", profile="deuteranopia")
pal.high.hex    # "#d55e00" (vermilion, safe for red-green confusion)

# Export for GTK CSS
css = to_gtk_css(RISK, prefix="risk-")
# .risk-low { color: #1a7f37; } ...

# Flat dict for JSON
RISK.to_dict()  # {"low": "#1a7f37", "medium": "#9a6700", "high": "#cf222e"}
```

## WCAG helpers

```python
from codechu_color import contrast_ratio, pick_text_color

contrast_ratio((255, 255, 255), (0, 0, 0))   # 21.0  (max)
pick_text_color((9, 105, 218))                # (255, 255, 255) — white on blue
```

## Built-in palettes

| name | keys |
|---|---|
| `RISK` | `low`, `medium`, `high` |
| `TERMINAL` | basic ANSI 8 |
| `MATERIAL` | Material Design Primary 500 tones |
| `SOLARIZED_LIGHT` / `SOLARIZED_DARK` | full accent ramp + base tones |

## Vision profiles

`palette_for("risk", profile=...)` accepts:

- `"default"` — GitHub semantic green / amber / red
- `"protanopia"` — safe for protan red-blindness
- `"deuteranopia"` — safe for deutan red-green confusion (most common)
- `"tritanopia"` — safe for tritan blue-yellow confusion

Profiles use the Bang & Wong (2011) qualitative palette
(*Nature Methods* 8: 441).

## License

MIT
