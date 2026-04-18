# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
