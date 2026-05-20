# CLAUDE.md — codechu-color

Bootstrap per `codechu-org/ai/AGENTS.md` §0 before any work. Prefer
the local clone at `$org_home/codechu-org/ai/AGENTS.md` (if
`~/.config/codechu/config.toml` has `org_home` set); otherwise
WebFetch the public raw URL
<https://raw.githubusercontent.com/codechu/codechu-org/main/ai/AGENTS.md>.
This file lists only product-local overrides.

## Product-local notes

- Pure stdlib color library. **No** external runtime dependencies.
- Public API: `Color`, `Palette`, `palette_for`, built-in palette
  constants (`RISK`, `TERMINAL`, `MATERIAL`, `SOLARIZED_LIGHT`,
  `SOLARIZED_DARK`), color-space helpers (`hex_to_rgb`, `rgb_to_hex`,
  `rgb_to_hsl`, `hsl_to_rgb`, `relative_luminance`, `contrast_ratio`,
  `pick_text_color`), and `to_gtk_css`. Module internals are not API.
- Palette hex values are part of the public contract. Changing a
  built-in palette colour is a breaking change.
- GTK adapter (`to_gtk_css`) must remain importable without GTK
  installed — it only emits CSS text.
- Coverage target: ≥90 %.

## Discipline reminders (org rules apply)

- Conventional Commits, no AI signature.
- No `--no-verify`, no force push, no unapproved publish.
- See `codechu-org/ai/AGENTS.md` for the full list.
