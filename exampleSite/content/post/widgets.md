+++
title       = "Sidebar widgets"
description = "Demonstrates the about, categories, tags, and ASCII-tree TOC widgets."
date        = 2026-04-10
categories  = ["general"]
tags        = ["widgets", "toc", "sidebar"]
+++

The sidebar loads widgets from `[params.widgets]` in `hugo.toml`. The
list is scoped per page kind: one for the homepage and taxonomy pages,
another for individual posts.

## Available widgets

### about

Pulls title and description from `[params.widgets.about]`.

### categories

Lists every category in the site with post counts. Linked to the
category taxonomy page.

### tags

Flat tag cloud rendered as inline chips: `[ tag ]`.

### toc

Walks `.Fragments.Headings` for the current page and emits an ASCII
tree:

```
├─ First heading
│  ├─ Subheading
│  └─ Subheading
└─ Last heading
```

Box-drawing characters are Unicode U+251C / U+2514 / U+2500 / U+2502.

## Scoping

Configure `[params.widgets.homepage]` and `[params.widgets.page]`
independently. A post without H2 headings gets no TOC widget.

## Writing your own

Drop an HTML template into `layouts/_partials/widget/<name>.html`,
add `{ type = "<name>" }` to the widget list, and the sidebar loader
picks it up. The template receives a dict with `Context` (the page)
and `Params` (whatever was on the widget entry).
