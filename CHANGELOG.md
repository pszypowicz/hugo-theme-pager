# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Add bullets here under `### Added`, `### Changed`, `### Fixed`, or `### Removed`
when a PR modifies theme behavior. On release, rename this heading to the new
version (dates are not tracked here; the git tag carries them), then push an
annotated tag `vX.Y.Z`; `.github/workflows/release.yml` turns the extracted
section into a GitHub Release body. Docs-only, CI-only, or meta-only PRs can
bypass the PR-side check via the `skip-changelog` label or a `[skip changelog]`
tag in the PR body; see `.github/workflows/changelog.yml`.

### Added

- Self-hosted ESLint and `tsc --checkJs` for `assets/js/`. The theme
  ships `package.json` (eslint + typescript devDeps, `lint` /
  `typecheck` scripts) and `eslint.config.mjs`, and `ci.yml` gains a
  `lint` job. Consumers on Hugo Modules (where the theme's JS source
  is not in the consumer tree) no longer need to re-host this tooling.

## [0.2.1]

### Changed

- README and `theme.toml` describe the theme accurately: system
  monospace for chrome + headings + code, humanist sans for body.
  Drops the "monospace-first" framing that never matched the CSS.
- README install section adds Hugo Modules as the recommended path,
  and the "zero JavaScript" bullet reflects that the production build
  ships a one-line inline preload-swap handler.
- Dropped the no-op `"ss01" 1` font-feature-setting on headings -
  a Cascadia stylistic set that has been dead since v0.2.0 removed
  the font.

### Fixed

- `kbd` elements and the dev debug overlay pills no longer have
  rounded corners, honoring the "no rounded cards" rule in the README.

### Removed

- Cascadia-Code credit in the README and a stale "Cascadia swaps in
  later" reference in `exampleSite/content/post/hello-world.md`, both
  left over after v0.2.0 dropped the font.

## [0.2.0]

### Changed

- `--mono-stack` falls through to `ui-monospace` / `SFMono-Regular`
  instead of pulling in Cascadia Code. The `font-display: optional`
  swap that drove the iPad Safari layout shift (fresh visit computed
  against the fallback, second visit against the cached webfont) no
  longer exists because there is no webfont.
- Real grid fix for the "main column shifts right on long code lines
  or wide TOC titles" iPad bug:
  `grid-template-columns: var(--col-aside) minmax(0, 1fr)`,
  `.main { overflow-x: hidden }`, `pre`/`.highlight { min-width: 0 }`.
  Together these stop descendant min-content from inflating the main
  track.
- Inline `<code>` drops the bottom border (previously read as a link)
  and gains muted backtick pseudo-elements. Matches the terminal
  voice and mirrors the Markdown source.

### Added

- Dev-only debug overlay at `layouts/_partials/debug.html`. Renders
  two pills when `hugo.IsServer` or `CF_PAGES_BRANCH != "main"`:
  a viewport / page-box / sidebar-box / main-box / computed grid
  template readout with tap-to-copy JSON, and an auto-reload toggle
  that polls the current URL every 5 s and reloads only when the
  modeline SHA changes. Scripts live in `assets/js/overlay.js` and
  `assets/js/autoreload.js`, minified and fingerprinted via
  `js.Build`. Production on `main` ships zero bytes of this.
- `jsconfig.json` enables strict `checkJs` across `assets/js/**`.
- `.github/workflows/ci.yml` builds `exampleSite/` on every PR as a
  lightweight sanity gate; actions/checkout pinned to v5.0.1 by SHA.
- `exampleSite/hugo.toml` allowlists `CF_PAGES_*` and `COMMIT_SHA` in
  `security.funcs.getenv` so the modeline footer's `os.Getenv` call
  clears Hugo's default policy on consumer sites.

### Removed

- `static/fonts/cascadia/*.woff2` (normal + italic variable faces),
  `assets/scss/_fonts.scss`, and the `@import "fonts"` in
  `rest.scss`. No more web fonts shipped.

## [0.1.9]

### Fixed

- iPad Safari sidebar-track inflation:
  `grid-template-columns: minmax(0, var(--col-aside)) 1fr` forces the
  sidebar track's minimum to zero so no descendant can widen it, and
  `min-width: 0` on `.sidebar` / `.sidebar-bot` breaks the flex chain
  so monospace min-content from TOC `<pre>` content cannot bubble up
  to the grid.

## [0.1.8]

### Changed

- Inline `<code>` loses the `border-bottom` that read as a link and
  gains `content` prefix / suffix in `--ink-3`.
- Modeline optionally links the build SHA to a GitHub tree URL via
  `Site.Params.repoURL`; falls back to a plain span when unset.

### Fixed

- `min-width: 0` on `.sidebar-col` to stop WebKit from expanding the
  fixed grid track when a TOC widget's non-wrapping content reports
  a larger min-content.

## [0.1.7]

### Changed

- `--col-aside` widened from `20ch` to `22ch` so longer TOC titles
  stop truncating on tablet widths.

## [0.1.6]

### Changed

- Primary and secondary sidebars rejoin into a single sticky column.
  `baseof.html` wraps `sidebar.html` + `sidebar-bot.html` in
  `<div class="sidebar-col">`; `_layout.scss` switches to a two-
  column grid (`var(--col-aside) 1fr`) and lets the wrapper stay
  sticky on desktop.

## [0.1.5]

### Added

- Post meta renders an `ai-assisted` badge when front matter sets
  `ai_assisted = true`. Ember accent, uppercase, small caps-tracking;
  `title=` attribute explains the disclosure.

## [0.1.4]

### Changed

- Split sidebar into two partials so mobile readers see articles
  before taxonomy. Primary widgets (about, toc) render in
  `<aside class="sidebar">` above `<main>`; secondary widgets render
  in `<aside class="sidebar-bot">` below it. On desktop, a
  `grid-template-areas` layout pins both asides to the left column,
  preserving the previous visual.
- Widgets opt into the secondary block with `position = "bot"` in
  site config. Anything without a `position` stays primary, so the
  change is source-compatible for existing sites.

### Added

- `layouts/_partials/sidebar-bot.html`. Only emits an `<aside>` when
  the current scope has at least one bot widget.

## [0.1.3]

### Changed

- Tighter TOC widget: line-height drops from 1.7 to 1.35 for a
  proper terminal feel.
- Each TOC entry now truncates with an ellipsis when longer than the
  sidebar (previously either clipped silently or wrapped and broke
  the tree alignment - both inconsistent).
- TOC anchors carry a `title=` attribute so the full heading text
  surfaces on hover for truncated entries.

## [0.1.2]

### Added

- Default favicon: the ember `§` glyph on warm paper with a
  dark-mode swap via `prefers-color-scheme`. Lives in
  `static/favicon.svg` (~500 B) plus a 180 px PNG for iOS at
  `static/apple-touch-icon.png`.
- `<link rel="icon">` and `<link rel="apple-touch-icon">` in
  `head/meta.html`. Sites that drop their own `favicon.svg` /
  `apple-touch-icon.png` into their own `static/` automatically
  override the theme defaults via Hugo's static-file resolution.

## [0.1.1]

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

## [0.1.0]

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
