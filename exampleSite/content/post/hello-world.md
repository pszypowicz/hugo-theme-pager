+++
title       = "Hello, world"
description = "First post of the example site - no code, just prose, to show how the ASCII TOC and modeline render."
date        = 2026-04-01
categories  = ["general"]
tags        = ["intro", "pager"]
+++

Welcome to the Pager example site. This post is pure prose so you can
see how the reading column caps at 80ch and how the modeline footer
reports word count and read time.

## Why another Hugo theme

Because most themes ship hundreds of kilobytes of JavaScript, a dozen
web fonts, and a full-featured search index - all before a single
character renders. Pager inverts the priorities.

## What matters

- **TCP initcwnd.** The first round-trip after the handshake carries
  about 14 KB of Brotli-q11 payload. Everything critical must fit.
- **System fonts first.** The reader sees text in under 200 ms.
  Cascadia Code swaps in later, without layout shift.
- **One column to read, one column to navigate.** The sidebar stays
  sticky on scroll; the main column stays short enough to follow.

### A note on taste

The accent color is ember. The paper is warm off-white. Borders are
hairlines. There are no shadows, no rounded corners, no cards.

## What's missing

Plenty, on purpose: search, comments, galleries, analytics, theme
toggles, and smooth scroll. Add what you need; skip what you don't.
