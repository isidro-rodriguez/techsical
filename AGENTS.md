# AGENTS.md

Instructions for AI agents working on **techsical**: tema editorial técnico para Zensical, publicado en PyPI.

The shared sections below are the same in every project. Project-specific rules are at the
end, under **Project rules**, and take precedence when they differ.

<!-- shared:start — managed by assistant-skills/new-python-project (scaffold.py sync). Edit there, not here. -->
## Shared rules

**Language.** Code and identifiers in English. Docstrings, comments, README, `docs/`,
CHANGELOG, commits and user-facing messages in Spanish. This file stays in English.

**Tools.** `uv` only, never `pip install`; run everything from the project root.
Quality gate: `uv run ruff format --check .`, `uv run ruff check .`, `uv run ty check`,
`uv run pytest`. The same gate as `poe check`, if Poe the Poet is installed globally; poe is
never a project dependency, and everything must also work with plain `uv run`.

**Workflow.**

1. Read `README.md`, `pyproject.toml`, this file and the related tests before changing code.
2. Make the smallest change that solves the task: no unrelated refactors, no formatting of
   untouched files, no new dependency without a reason (prefer the standard library).
3. Don't change CI, tool configuration or project structure unless the task needs it.
4. Don't run a failing command more than twice: stop, give the root cause and the exact error,
   propose the minimal fix and ask.
5. Don't run state-changing git commands (commit, push, tag, reset, rebase) unless the user
   asks or the commit policy in **Project rules** allows it. Never `--no-verify`.
6. Leave no secrets, temporary files or TODOs without context. Never hand-edit `uv.lock`.

**Code.** Strict type hints on every signature. Google-style docstrings: complete for public
identifiers, one line for private ones; a public docstring's `Raises` also lists the
exceptions raised by the private functions it calls. Comments explain the *why*. Prefer
simple, explicit code; `pathlib` over `os.path`. Ruff and ty enforce the rest; don't fight
them with ignores.

**Tests.** `pytest` in `tests/`. Cover relevant logic and every fixed bug; they must pass on
Linux and Windows.

**Commits.** Conventional Commits in Spanish (`feat:`, `fix:`, `docs:`, `test:`,
`refactor:`, `chore:`), one intent per commit, explaining the *why*.

**Releases.** Only for versioned projects (a real version and `CHANGELOG.md`). Before
pushing changes to the package, use the `python-release` skill. Without it: SemVer bump,
`## [Unreleased]` → `## [X.Y.Z] - YYYY-MM-DD` in `CHANGELOG.md`, `uv lock`, then
`chore: bump versión a X.Y.Z`. Never tag without confirmation.

**Done** when the quality gate and any extra gate in **Project rules** pass, and the README
and docs reflect any change in usage.

Project rules below take precedence over these. Shared rules change in assistant-skills
(`scaffold.py sync`), not by hand here.
<!-- shared:end -->

## Project rules

techsical is a Zensical theme published on PyPI. It extends Zensical's own theme
(`extends: zensical`) and is used by the documentation sites of acodo, pyMedia, atril
and reCocina. Design brief: `Tema.md` in the "Skills" claude.ai project (Technical
Editorial Design System), scoped to static documentation sites.

### Structure

```
src/techsical/
├── __init__.py          # THEME_DIR and `theme`, the object the entry point registers
└── theme/               # the theme folder Zensical reads (no Python files here)
    ├── mkdocs_theme.yml # extends: zensical; language, font: false, features, palette
    ├── home.html        # front page (template: home.html, `hero:` front matter)
    ├── partials/        # icons.html (head hook), techsical-head.html, header.html,
    │                    #   copyright.html
    └── assets/          # stylesheets/techsical.css + fonts.css, fonts/ (woff2 + OFL)
docs/ + zensical.toml    # demo site and user guide, built with the theme itself
docs_templates/          # demo only: Spanish mkdocstrings templates (es.html.jinja)
examples/obra/           # demo only: sample package for the API reference pages
scripts/capturas.py      # Playwright screenshots of the demo site (light/dark, desktop/mobile)
tests/                   # builds sites with the theme; WCAG contrast of the colours
```

### Theme rules

- Zensical finds the theme through the `mkdocs.themes` entry point
  (`techsical = "techsical:theme"`) and copies every non-template file of the theme
  folder into the site, so `theme/` must never contain Python or other stray files.
- Never override `main.html`: sites override it (reCocina). Head content goes through
  `partials/icons.html` (included by `base.html` inside `<head>`), which includes
  `partials/techsical-head.html`.
- Overridden Zensical templates are copies: `partials/icons.html`, `header.html` and
  `copyright.html`. Each starts with a comment naming the Zensical theme version it was
  copied from and marks its changes with «techsical». On every Zensical upgrade, diff
  them against the new theme and port the changes. Keep this list short.
- The `zensical` dependency range stays narrow (`>=X.Y.Z,<0.(Y+1)`): Zensical warns that
  its theming system will change with components.
- Sites customise only through `[project.extra.techsical]` (documented in
  `docs/guia/personalizacion.md` and at the top of `techsical-head.html`) or their own
  stylesheet, which loads after the theme's.
- CSS variables in layers: primitives (`--tx-petroleum-*`…), brand (`--tx-brand-*`),
  semantic per scheme (`--tx-text`, `--tx-surface-*`…), bridge to Zensical's `--md-*`,
  components. Components use semantic variables only, never raw hex.
- Fonts: Source Serif 4 for body text and headings, Manrope for interface, tables,
  captions and labels, JetBrains Mono for code. Variable woff2 (latin, latin-ext, greek)
  from Fontsource, OFL licences next to them; `fonts.css` is generated from Fontsource's
  CSS, not hand-edited.
- Images are centred blocks, never upscaled (`max-width`, no `width`); tables take the
  full article width; the TOC is hidden per page with `hide: [toc]`.
- Keep `tests/test_contrast.py` in sync with the colours: every text/background pair
  the theme uses must reach WCAG AA (4.5:1 text, 3:1 large text and icons).
- Visual changes: build the demo site and run `scripts/capturas.py`; the user reviews
  the screenshots before a release.

### Extra quality gates

- `uv run zensical build` must end with "No issues found" (the tests also build sites).
- CI (`.github/workflows/ci.yml`): ruff, ty and pytest on ubuntu and windows.

### Commit policy

Never commit automatically: report the result and wait for confirmation.

### Publishing

`publish.yml` publishes to PyPI (trusted publishing) on every push to `main` that touches
`src/`, `pyproject.toml`, `README.md` or `LICENSE`, unless the tag `vX.Y.Z` of the
current version already exists; it then creates the tag and a GitHub release. A push that
changes the package must bump the version (shared **Releases** rules). `docs.yml`
publishes the demo site to GitHub Pages.
