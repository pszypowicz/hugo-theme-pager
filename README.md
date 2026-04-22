# Pager

A Hugo theme built around a single performance rule: **the critical path of every page fits in the first TCP flight after the handshake (~14 KB Brotli-q11).**

Pager is terminal-styled, opinionated, and purpose-built for technical writing. Chrome, headings, and code are set in the platform's monospace (`ui-monospace` / SF Mono / Cascadia Mono / Consolas); body paragraphs stay in the system humanist sans for comfortable long-form reading. It ships:

- **No JavaScript on the production critical path.** The only client-side JS on `main` is a one-line inline `onload` handler that promotes the deferred stylesheet `<link>` from `preload` to `stylesheet`. A small debug overlay ships on `hugo server` and non-`main` Cloudflare Pages preview branches only (see `layouts/_partials/debug.html`); production builds emit zero overlay bytes.
- **Zero web fonts.** No `@font-face`, no `<link rel="preload" as="font">`, no `.woff2` shipped. The system stack renders immediately and stays; nothing swaps in later, so there is no CLS race and no per-OS layout divergence.
- **Inlined critical CSS**, external deferred stylesheet with immutable cache.
- **Single left sidebar** carrying header, menu, and contextual widgets (categories / tags / TOC). Main column caps at 80ch.
- **ASCII-tree table of contents** instead of nested bullet lists.
- **Modeline footer** rendered like vim's status bar.
- **Print stylesheet** that turns posts into readable technical papers.

## Aesthetic

Ember/terracotta accent on warm off-white paper (light) or deep ink (dark). `prefers-color-scheme` selects. No purple, no shadows, no rounded cards. Borders where structure demands, negative space elsewhere. Monospace drives the chrome and the headings; body copy flows in a humanist sans against the same grid.

| Light                           | Dark                                |
| ------------------------------- | ----------------------------------- |
| ![light](images/screenshot.png) | ![dark](images/screenshot-dark.png) |

## Requirements

- Hugo extended >= 0.160.0 (uses `.Fragments.Headings` and `resources.Fingerprint`).

## Install

As a Hugo Module (recommended). From the root of your site:

```
hugo mod init github.com/you/your-site
```

Then in `hugo.toml`:

```toml
[module]
  [[module.imports]]
    path = "github.com/pszypowicz/hugo-theme-pager"
```

Followed by `hugo mod get -u`.

Or as a git submodule:

```
git submodule add https://github.com/pszypowicz/hugo-theme-pager.git themes/pager
```

Then in `hugo.toml`:

```toml
theme = "pager"
```

## Quick start

The fastest way to see Pager end-to-end is to copy the bundled example:

```
hugo new site my-blog
cd my-blog
git submodule add https://github.com/pszypowicz/hugo-theme-pager.git themes/pager
cp themes/pager/exampleSite/hugo.toml .
cp -R themes/pager/exampleSite/content/* content/
hugo server
```

`exampleSite/hugo.toml` is a full working config (widgets, menus, markup, permalinks); `exampleSite/content/` has three posts and an about page.

## Parameters

See `exampleSite/hugo.toml` for the full set. Widgets live under `[params.widgets]`:

```toml
[params]
  mainSections = ["post"]

  [params.sidebar]
    subtitle = "Hitchhiking through raw bits"

  [[params.widgets.homepage]]
    type = "about"

  [[params.widgets.homepage]]
    type = "categories"

  [[params.widgets.homepage]]
    type = "tags"

  [[params.widgets.page]]
    type = "about"

  [[params.widgets.page]]
    type = "toc"
```

## Non-goals

Search, comments, galleries, analytics, theme switcher UI, multilingual switcher UI, mermaid diagrams, and smooth-scroll. All deliberately absent. Add them yourself if you need them.

## Credits

- Icon paths derived from [Tabler Icons](https://tabler.io/icons) - MIT.

## License

MIT. See [`LICENSE`](./LICENSE).
