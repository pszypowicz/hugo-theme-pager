#!/usr/bin/env node
// Render the bundled exampleSite home page and write the gallery
// screenshots referenced from README.md and theme.toml. Builds the
// site into a temporary directory, serves it over an ephemeral local
// HTTP port so subresources resolve normally, then drives a headless
// chromium through three viewport / colour-scheme combinations.
//
// Run with `npm run screenshots` or `node scripts/capture-screenshots.mjs`.
// `--help` prints usage.

import { parseArgs } from "node:util";
import { spawnSync } from "node:child_process";
import { createServer } from "node:http";
import { mkdtemp, rm, stat, readFile, symlink, mkdir } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join, extname, resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = resolve(SCRIPT_DIR, "..");

const CAPTURES = [
  { name: "screenshot.png",      width: 1500, height: 1000, colorScheme: "light" },
  { name: "screenshot-dark.png", width: 1500, height: 1000, colorScheme: "dark"  },
  { name: "tn.png",              width:  900, height:  600, colorScheme: "light" },
];

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".css":  "text/css; charset=utf-8",
  ".js":   "application/javascript; charset=utf-8",
  ".mjs":  "application/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg":  "image/svg+xml",
  ".png":  "image/png",
  ".jpg":  "image/jpeg",
  ".jpeg": "image/jpeg",
  ".gif":  "image/gif",
  ".ico":  "image/x-icon",
  ".woff": "font/woff",
  ".woff2":"font/woff2",
  ".txt":  "text/plain; charset=utf-8",
  ".xml":  "application/xml; charset=utf-8",
};

const HELP = `Usage: node scripts/capture-screenshots.mjs [options]

Capture the gallery screenshots from the bundled exampleSite home page.
Builds exampleSite with hugo, serves it locally, drives a headless
chromium to render three viewports, writes PNGs to --out-dir.

Options:
  --out-dir <path>    Directory to write the PNGs into (default: images)
  --hugo <path>       hugo binary to use (default: hugo on PATH)
  --keep-temp         Leave the built site on disk after exit (default: remove)
  -h, --help          Show this help and exit

Outputs (relative to --out-dir):
  screenshot.png       1500x1000, light colour scheme
  screenshot-dark.png  1500x1000, dark colour scheme
  tn.png                900x600,  light colour scheme

Requires: hugo on PATH (or --hugo), playwright with chromium installed
(\`npm install\` followed by \`npx playwright install chromium\`).
`;

function parseCli() {
  let args;
  try {
    args = parseArgs({
      options: {
        "out-dir":   { type: "string", default: "images" },
        "hugo":      { type: "string", default: "hugo"   },
        "keep-temp": { type: "boolean", default: false   },
        "help":      { type: "boolean", short: "h", default: false },
      },
      strict: true,
    });
  } catch (err) {
    process.stderr.write(`error: ${err.message}\n\n${HELP}`);
    process.exit(2);
  }
  if (args.values.help) {
    process.stdout.write(HELP);
    process.exit(0);
  }
  return {
    outDir:   resolve(REPO_ROOT, args.values["out-dir"]),
    hugoBin:  args.values.hugo,
    keepTemp: args.values["keep-temp"],
  };
}

async function buildSite({ hugoBin, destDir, themesDir }) {
  // exampleSite/hugo.toml declares `theme = "pager"`, so hugo expects
  // a directory named `pager` under --themesDir. The repo itself is
  // `hugo-theme-pager`, which is fine in CI (checkout uses path: pager)
  // but not when running from a normal clone. Stage a symlink so the
  // lookup succeeds regardless of the on-disk directory name.
  await mkdir(themesDir, { recursive: true });
  await symlink(REPO_ROOT, join(themesDir, "pager"), "dir");

  const result = spawnSync(
    hugoBin,
    [
      "--source", join(REPO_ROOT, "exampleSite"),
      "--themesDir", themesDir,
      "--destination", destDir,
      "--minify",
      "--gc",
      "--cleanDestinationDir",
    ],
    { stdio: "inherit" },
  );
  if (result.error) {
    throw new Error(`failed to spawn ${hugoBin}: ${result.error.message}`);
  }
  if (result.status !== 0) {
    throw new Error(`${hugoBin} exited with status ${result.status}`);
  }
}

function startStaticServer(rootDir) {
  const server = createServer(async (req, res) => {
    try {
      const url = new URL(req.url, "http://localhost/");
      let pathname = decodeURIComponent(url.pathname);
      if (pathname.endsWith("/")) pathname += "index.html";
      const target = join(rootDir, pathname);
      if (!target.startsWith(rootDir)) {
        res.writeHead(403).end("forbidden");
        return;
      }
      let body;
      let resolvedPath = target;
      try {
        const s = await stat(target);
        if (s.isDirectory()) resolvedPath = join(target, "index.html");
      } catch {
        res.writeHead(404).end("not found");
        return;
      }
      try {
        body = await readFile(resolvedPath);
      } catch {
        res.writeHead(404).end("not found");
        return;
      }
      const type = MIME[extname(resolvedPath).toLowerCase()] || "application/octet-stream";
      res.writeHead(200, { "content-type": type, "content-length": body.length });
      res.end(body);
    } catch (err) {
      res.writeHead(500).end(`server error: ${err.message}`);
    }
  });
  return new Promise((resolveListen, rejectListen) => {
    server.once("error", rejectListen);
    server.listen(0, "127.0.0.1", () => {
      const addr = server.address();
      resolveListen({ server, port: addr.port });
    });
  });
}

async function capture({ port, outDir }) {
  const { chromium } = await import("playwright");
  const browser = await chromium.launch();
  try {
    for (const shot of CAPTURES) {
      const context = await browser.newContext({
        viewport: { width: shot.width, height: shot.height },
        colorScheme: shot.colorScheme,
        deviceScaleFactor: 1,
      });
      const page = await context.newPage();
      await page.goto(`http://127.0.0.1:${port}/`, { waitUntil: "networkidle" });
      const out = join(outDir, shot.name);
      await page.screenshot({ path: out, fullPage: false, type: "png" });
      await context.close();
      process.stdout.write(`wrote ${out} (${shot.width}x${shot.height}, ${shot.colorScheme})\n`);
    }
  } finally {
    await browser.close();
  }
}

async function main() {
  const opts = parseCli();
  const workDir = await mkdtemp(join(tmpdir(), "pager-screenshots-"));
  const siteDir = join(workDir, "site");
  const themesDir = join(workDir, "themes");
  let server;
  try {
    await buildSite({ hugoBin: opts.hugoBin, destDir: siteDir, themesDir });
    const started = await startStaticServer(siteDir);
    server = started.server;
    await capture({ port: started.port, outDir: opts.outDir });
  } finally {
    if (server) await new Promise((r) => server.close(r));
    if (!opts.keepTemp) {
      await rm(workDir, { recursive: true, force: true });
    } else {
      process.stdout.write(`kept build dir: ${workDir}\n`);
    }
  }
}

main().catch((err) => {
  process.stderr.write(`error: ${err.message}\n`);
  process.exit(1);
});
