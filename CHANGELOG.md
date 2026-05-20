# Changelog

[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) + [SemVer](https://semver.org/).

## [Unreleased]

## [0.1.0] — 2026-05-20

### Added
- `Color` — single color with ANSI / hex / RGB / RGBA forms,
  constructible via `Color.from_hex`, `Color.from_rgb`, or direct
  field access.
- `Palette` — named collection of `Color` values with attribute
  access, `to_dict()` flat export, and iteration.
- Five built-in palettes: `RISK` (GitHub semantic green/amber/red),
  `TERMINAL` (basic ANSI 8), `MATERIAL` (Material Design Primary 500
  tones), `SOLARIZED_LIGHT`, `SOLARIZED_DARK`.
- `palette_for(name, *, profile=...)` — color-blind safe variants
  using the Bang & Wong (2011) qualitative palette (*Nature Methods*
  8: 441). Profiles: `"default"`, `"protanopia"`, `"deuteranopia"`,
  `"tritanopia"`.
- Conversion helpers: `hex_to_rgb`, `rgb_to_hex`, `rgb_to_hsl`,
  `hsl_to_rgb`.
- WCAG helpers: `relative_luminance`, `contrast_ratio`,
  `pick_text_color` — implements WCAG 2.1 §1.4.3 contrast formula.
- GTK adapter: `to_gtk_css(palette, prefix=...)` — emits a CSS string
  with one class rule per color, suitable for `Gtk.CssProvider`.

### Notes
- Stdlib-only. No external runtime dependencies.
- Python 3.10+.

[Unreleased]: https://github.com/codechu/color-py/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/codechu/color-py/releases/tag/v0.1.0
