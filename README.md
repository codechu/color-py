```text
   c o d e c h u  ·  c o l o r
   ███  ▓▓▓  ▒▒▒  ░░░    #1a7f37   #9a6700   #cf222e
   ░░░  ▒▒▒  ▓▓▓  ███    rgb · hex · ansi · gtk-css
   ── one palette. every surface. every eye. ──
```

[![PyPI](https://img.shields.io/pypi/v/codechu-color.svg)](https://pypi.org/project/codechu-color/)
[![Python](https://img.shields.io/pypi/pyversions/codechu-color.svg)](https://pypi.org/project/codechu-color/)
[![CI](https://github.com/codechu/color-py/actions/workflows/ci.yml/badge.svg)](https://github.com/codechu/color-py/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> *Stdlib-only color palettes, conversions, and WCAG helpers — colour-blind safe variants included.*

# codechu-color

One source of truth for color across surfaces. CLI tools want ANSI
escapes, GTK / web apps want hex and CSS, JSON exports want flat
dicts, accessibility audits want WCAG contrast and color-blind-safe
variants. `codechu-color` keeps the palette in one place and derives
every form.

```text
        default      protanopia    deuteranopia   tritanopia
low     ▓ #1a7f37    ▓ #117733     ▓ #009e73      ▓ #44aa99
med     ▓ #9a6700    ▓ #cc6677     ▓ #e69f00      ▓ #ddcc77
high    ▓ #cf222e    ▓ #882255     ▓ #d55e00      ▓ #cc6677
```

## Install

```bash
pip install codechu-color
```

Python 3.10+. Zero third-party dependencies.

## Quick example

```python
from codechu_color import Color, RISK, palette_for, contrast_ratio, to_gtk_css

# One color, every form
green = Color.from_hex("#1a7f37", name="low")
green.rgb       # (26, 127, 55)
green.ansi_fg   # "\x1b[32m"

# Built-in semantic palette (GitHub accessibility-tuned)
RISK.high.hex   # "#cf222e"

# Color-blind safe variant
pal = palette_for("risk", profile="deuteranopia")
pal.high.hex    # "#d55e00" (vermilion, safe for red-green confusion)

# Export for GTK CSS
to_gtk_css(RISK, prefix="risk-")

# WCAG helpers
contrast_ratio((255, 255, 255), (0, 0, 0))   # 21.0 (max)
```

## What you get

- **`Color`** — single color with `.rgb`, `.hex`, `.ansi_fg`,
  `.ansi_bg` views and `.from_hex` / `.from_rgb` constructors.
- **Built-in palettes** — `RISK` (low/medium/high, GitHub-tuned),
  `TERMINAL` (ANSI 8), `MATERIAL`, `SOLARIZED_LIGHT` /
  `SOLARIZED_DARK`.
- **Color-blind safe variants** — `palette_for(name, profile=…)`
  with `default` / `protanopia` / `deuteranopia` / `tritanopia`,
  using the Bang & Wong (2011) qualitative palette.
- **WCAG helpers** — `contrast_ratio()`, `pick_text_color()` for
  picking readable foreground over an arbitrary background.
- **Export helpers** — `to_gtk_css(palette, prefix=…)`,
  `palette.to_dict()` for JSON.

## Read more

- [API reference](docs/API.md) — every public symbol with
  signatures and edge-case tables.
- [Changelog](CHANGELOG.md)

## Family

| Library | Purpose |
|---------|---------|
| [codechu-cli](https://pypi.org/project/codechu-cli/) | CLI primitives — colors, progress, prompts |
| [codechu-term](https://pypi.org/project/codechu-term/) | Terminal capabilities, alt buffer, raw mode |
| [codechu-spark](https://pypi.org/project/codechu-spark/) | Unicode sparklines, mini bar charts, heatmaps |
| [codechu-fmt](https://pypi.org/project/codechu-fmt/) | Human-readable sizes, durations, rates |
| [codechu-treeviz](https://pypi.org/project/codechu-treeviz/) | Treemap + sunburst layouts |

Full ecosystem: [github.com/codechu](https://github.com/codechu).

## Credits

- Color-blind safe palettes based on Bang & Wong (2011),
  *Nature Methods* 8:441.
- Risk semantic colors match GitHub's accessibility-tuned palette.
- WCAG contrast ratio formula from W3C WCAG 2.1 guidelines.

## License

MIT — see [LICENSE](LICENSE).

Part of [Codechu](https://github.com/codechu).
