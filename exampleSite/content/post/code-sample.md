+++
title       = "Rendering a code block"
description = "Shows how chroma syntax highlighting renders under Pager's deferred stylesheet."
date        = 2026-04-05
categories  = ["general"]
tags        = ["code", "pager", "syntax"]
+++

Code blocks are rendered by chroma at build time. The syntax palette
is part of the deferred stylesheet (`rest.scss`), so the first paint
never waits on it.

## Shell

```sh
#!/bin/sh
set -eu
host=$(hostname)
printf 'serving %s\n' "$host"
```

## Go

```go
package main

import "fmt"

func main() {
    msg := "hello from pager"
    fmt.Println(msg)
}
```

## TOML

```toml
[params.widgets]
    page = [
        { type = "about" },
        { type = "toc" },
    ]
```

## Inline

A `monospace` run inside prose uses the same ember border-left as a
full block, but without the gutter. Keyboard hints render as
<kbd>Ctrl</kbd>+<kbd>C</kbd>.
