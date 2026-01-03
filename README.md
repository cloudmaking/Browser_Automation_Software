# AutoChrome 8 (Playwright)

A small, single-file CLI that runs browser automations from JSON steps or a single test line. It keeps a persistent profile folder so you can log in once and reuse sessions.

## Project goals (roadmap)

- Keep setup friction low: one CLI file, one profile folder, minimal deps.
- Preserve persistent Chrome profiles so logins stick across runs.
- Make automation authoring fast: JSON steps and single-line test commands.
- Add a Chrome extension recorder to capture selectors from real pages.
- Use extension output to generate precise action steps (favor stable selectors).
- Support flexible text matching but default to precise selectors.
- Improve reliability with clear errors, screenshots on failure, and strict validation.
- Later: let the extension append steps to a flow file and preview in-app.

## What you get

- Persistent profile folder (log in once, reuse sessions)
- JSON step runner
- Single-line test command for quick checks
- Headed or headless runs
- Chrome extension recorder for selectors

## Folder layout

- `autochrome8.py` - the runner
- `examples/` - sample flows
- `autochrome_profile/` - created on first run (default)
- `extension/` - Chrome extension recorder
- `old/` - legacy files from AutoChrome 6/7

## Setup

Create and activate a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
python -m playwright install
```

If you want to use your installed Chrome instead of Playwright's Chromium, add `--channel chrome` to commands.

## Quick start

1) Open a profile window to log in

```bash
python autochrome8.py profile --profile ./autochrome_profile --channel chrome
```

Log in to any sites you need, then press Enter in the terminal to close the window.

2) Run a JSON flow

```bash
python autochrome8.py run examples/quick_check.json --profile ./autochrome_profile --channel chrome
```

3) Test a single action line

```bash
python autochrome8.py test "click css='a'" --profile ./autochrome_profile --channel chrome
```

Single-line syntax uses key=value pairs:

```bash
python autochrome8.py test "fill css='input[name=email]' value='me@example.com'" --profile ./autochrome_profile
python autochrome8.py test "wait text='Example Domain' match=exact" --profile ./autochrome_profile
```

## Action format (JSON)

Each step is a single-key object. Supported actions:

- `goto`: string URL, or `{ "url": "...", "timeout_ms": 15000 }`
- `click`: `{ "css": "..." }` or `{ "xpath": "..." }` or `{ "text": "..." }`
- `fill`: selector plus `value`, e.g. `{ "css": "input[name=email]", "value": "me@example.com" }`
- `wait_for`: selector plus optional `timeout_ms` or `state` (`attached`, `visible`, `hidden`, `detached`)
- `sleep_ms`: number of milliseconds

Text matching options (for `text` selectors):

- `match`: `"exact"` or `"contains"` (default: contains)
- `exact`: `true` or `false` (alias for `match`)

Example:

```json
[
  {"goto": "https://example.com"},
  {"wait_for": {"text": "Example Domain"}},
  {"click": {"css": "a"}},
  {"wait_for": {"text": "IANA"}}
]
```

## Notes on profiles

- The profile folder can be any path; use an empty folder if you want a clean automation profile.
- If you point at a real Chrome user data directory, make sure Chrome is closed and use `--channel chrome`.
- The default profile path is `./autochrome_profile` (created on first run).

## Legacy

Older Selenium/Tkinter versions live in `old/` for reference.

## Chrome extension recorder

There is a simple extension to capture selectors and generate AutoChrome steps in `extension/`.

Load it in Chrome:

1) Open `chrome://extensions`
2) Enable Developer mode
3) Click "Load unpacked" and select the `extension/` folder

Usage:

1) Pick an action (click/fill/wait) in the popup
2) Click "Record", then click the element on the page
3) Reopen the popup to copy the JSON step or CLI line

Tip: open the same profile folder you use for automation, then load the extension there so it stays available in your automation profile.
