# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.3] - 2026-04-18

### Changed

- Tighter TOC widget: line-height drops from 1.7 to 1.35 for a
  proper terminal feel.
- Each TOC entry now truncates with an ellipsis when longer than the
  sidebar (previously either clipped silently or wrapped and broke
  the tree alignment - both inconsistent).
- TOC anchors carry a `title=` attribute so the full heading text
  surfaces on hover for truncated entries.

[0.1.3]: https://github.com/pszypowicz/hugo-theme-pager/releases/tag/v0.1.3

## [0.1.2] - 2026-04-18

### Added

- Default favicon: the ember `§` glyph on warm paper with a
  dark-mode swap via `prefers-color-scheme`. Lives in
  `static/favicon.svg` (~500 B) plus a 180 px PNG for iOS at
  `static/apple-touch-icon.png`.
- `<link rel="icon">` and `<link rel="apple-touch-icon">` in
  `head/meta.html`. Sites that drop their own `favicon.svg` /
  `apple-touch-icon.png` into their own `static/` automatically
  override the theme defaults via Hugo's static-file resolution.

[0.1.2]: https://github.com/pszypowicz/hugo-theme-pager/releases/tag/v0.1.2

## [0.1.1] - 2026-04-18

### Fixed

- Tag and category widgets now sort alphabetically. They ranged a Go
  map and so picked a new visit order on every build.
- About widget no longer renders an empty `<section>` when
  `[params.widgets.about].description` is unset.
- Print stylesheet suppresses the `§` prefix on H2/H3 headings; the
  glyph is decoration for screen reading, not content for paper.
- Icon helper renders the icon name as visible text for unknown
  names so a misconfigured social link is at least debuggable
  instead of silently invisible.

### Added

- `rel="prev"` / `rel="next"` on list pagination links for browsers,
  screen readers, and search engines.

[0.1.1]: https://github.com/pszypowicz/hugo-theme-pager/releases/tag/v0.1.1

## [0.1.0] - 2026-04-18

First public release.

### Added

- Layouts: `baseof`, `home`, `list`, `single`, `404`, partials for
  sidebar, footer (vim modeline), head meta/style, widget loader.
- Widgets: `about`, `categories`, `tags`, `toc` (ASCII-tree).
- Inline SVG icon sprite at `_partials/helper/icon.html` with
  `brand-github`, `brand-linkedin`, `rss`, `link` (Tabler-derived).
- SCSS split into inline critical (`critical.scss`: tokens, reset,
  typography, layout, widgets, article, modeline) and hashed deferred
  (`rest.scss`: code, chroma syntax, Cascadia @font-face, print).
- Cascadia Code variable WOFF2 (normal + italic) under
  `static/fonts/cascadia/`, loaded with `font-display: optional` and
  metric overrides for zero CLS.
- RSS feed auto-discovery via `<link rel="alternate">` in `head/meta`.
- `.Summary` fallback on list pages when a post has no description.
- exampleSite: complete `hugo.toml`, three sample posts, About page.
- Screenshots for the themes.gohugo.io gallery (`images/screenshot.png`,
  `images/tn.png`).

### Performance

- Zero JavaScript on first paint.
- Zero web fonts on first paint (system stack renders; Cascadia swaps
  after cache).
- Inline critical CSS, external deferred stylesheet with immutable
  cache.
- Designed to fit under the 14 KB TCP initcwnd after Brotli-q11.

[0.1.0]: https://github.com/pszypowicz/hugo-theme-pager/releases/tag/v0.1.0
