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

## Documentation

- [API reference](docs/API.md) — every public symbol, signatures, edge cases

## Codechu family

Companion libraries from the Codechu Python ecosystem:

| Library | Purpose |
|---------|---------|
| [codechu-fmt](https://pypi.org/project/codechu-fmt/) | Human-readable formatting — sizes, durations, rates, percent |
| [codechu-meter](https://pypi.org/project/codechu-meter/) | Timing primitives — Stopwatch, ETA, percentile, histogram |
| [codechu-spark](https://pypi.org/project/codechu-spark/) | Unicode sparklines, mini bar charts, heatmaps |
| [codechu-cli](https://pypi.org/project/codechu-cli/) | CLI primitives — colors, progress, spinners, prompts, table |
| [codechu-events](https://pypi.org/project/codechu-events/) | Thread-safe multi-channel pub/sub bus with replay |
| [codechu-xdg](https://pypi.org/project/codechu-xdg/) | XDG Base Directory helpers, vendor-namespaced |
| [codechu-treeviz](https://pypi.org/project/codechu-treeviz/) | Tree visualization — treemap, sunburst, icicle, flame |
| [codechu-fs](https://pypi.org/project/codechu-fs/) | Filesystem primitives — atomic write, XDG trash, safe walk |
| [codechu-term](https://pypi.org/project/codechu-term/) | Terminal capability detection, alt buffer, raw mode |
| [codechu-treedata](https://pypi.org/project/codechu-treedata/) | N-ary tree data structures and algorithms |
| [codechu-log](https://pypi.org/project/codechu-log/) | Structured logging — context, JSON, rotation, redaction |
| [codechu-i18n](https://pypi.org/project/codechu-i18n/) | Internationalization — locale, plural rules, RTL |
| [codechu-ipc](https://pypi.org/project/codechu-ipc/) | Local IPC — Unix socket, FIFO, JSON-line protocol |
| [codechu-config](https://pypi.org/project/codechu-config/) | Schema-driven config — atomic save, migrations |

## Credits

- Color-blind safe palettes based on Bang & Wong (2011), *Nature Methods* 8:441
- Risk semantic colors match GitHub's accessibility-tuned palette
- WCAG contrast ratio formula from W3C WCAG 2.1 guidelines

## License

MIT
