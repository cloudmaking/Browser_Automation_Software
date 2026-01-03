#!/usr/bin/env python3
import argparse
import json
import os
import shlex
import sys
import time
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

SELECTOR_KEYS = ("css", "xpath", "text")
DEFAULT_TIMEOUT_MS = 10000


def normalize_profile_dir(path: str) -> Path:
    expanded = Path(os.path.expanduser(path))
    if not expanded.is_absolute():
        expanded = (Path.cwd() / expanded).resolve()
    return expanded


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def parse_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in ("true", "1", "yes", "y"):
            return True
        if lowered in ("false", "0", "no", "n"):
            return False
    raise ValueError(f"Expected boolean, got '{value}'")


def parse_kv_args(tokens):
    data = {}
    for token in tokens:
        if "=" not in token:
            raise ValueError(f"Expected key=value, got '{token}'")
        key, value = token.split("=", 1)
        key = key.strip()
        if key in ("timeout_ms", "sleep_ms"):
            try:
                data[key] = int(value)
            except ValueError as exc:
                raise ValueError(f"{key} expects an integer, got '{value}'") from exc
        elif key == "exact":
            data[key] = parse_bool(value)
        elif key == "match":
            data[key] = value.strip().lower()
        else:
            data[key] = value
    return data


def parse_action_line(line: str):
    tokens = shlex.split(line)
    if not tokens:
        raise ValueError("Empty action")

    action = tokens[0].lower()
    if action == "goto":
        if len(tokens) != 2:
            raise ValueError("goto expects a single URL")
        return {"goto": tokens[1]}

    if action in ("click", "wait"):
        if len(tokens) < 2:
            raise ValueError(f"{action} expects selector arguments")
        payload = parse_kv_args(tokens[1:])
        key = "wait_for" if action == "wait" else "click"
        return {key: payload}

    if action == "fill":
        if len(tokens) < 3:
            raise ValueError("fill expects selector args and value=...")
        payload = parse_kv_args(tokens[1:])
        return {"fill": payload}

    if action in ("sleep", "sleep_ms"):
        if len(tokens) != 2:
            raise ValueError("sleep expects a number")
        if action == "sleep":
            seconds = float(tokens[1])
            return {"sleep_ms": int(seconds * 1000)}
        return {"sleep_ms": int(tokens[1])}

    raise ValueError(f"Unknown action '{action}'")


def load_steps(path: str):
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError("Flow file must be a JSON list")
    return data


def resolve_text_exact(extra):
    if not extra:
        return False
    if "match" in extra:
        match_value = str(extra["match"]).strip().lower()
        if match_value in ("exact", "equals"):
            return True
        if match_value in ("contains", "partial"):
            return False
        raise ValueError("match must be 'exact' or 'contains'")
    if "exact" in extra:
        return parse_bool(extra["exact"])
    return False


def build_locator(page, selector, extra=None):
    if "css" in selector:
        return page.locator(selector["css"])
    if "xpath" in selector:
        return page.locator(f"xpath={selector['xpath']}")
    if "text" in selector:
        exact = resolve_text_exact(extra)
        return page.get_by_text(selector["text"], exact=exact)
    raise ValueError("Selector must include css, xpath, or text")


def split_selector(payload):
    if not isinstance(payload, dict):
        raise ValueError("Selector payload must be an object with css/xpath/text")
    selector = {k: payload[k] for k in SELECTOR_KEYS if k in payload}
    if len(selector) > 1:
        raise ValueError("Selector must use only one of css, xpath, or text")
    extra = {k: v for k, v in payload.items() if k not in selector}
    if not selector:
        raise ValueError("Selector must include css, xpath, or text")
    return selector, extra


def save_error_screenshot(page):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"autochrome8_error_{timestamp}.png"
    try:
        page.screenshot(path=filename, full_page=True)
        return filename
    except Exception:
        return None


def run_steps(page, steps, default_timeout_ms):
    page.set_default_timeout(default_timeout_ms)
    total = len(steps)

    for idx, step in enumerate(steps, start=1):
        if not isinstance(step, dict) or len(step) != 1:
            raise ValueError(f"Step {idx} must be a single-key object")

        action, payload = next(iter(step.items()))
        print(f"[{idx}/{total}] {action}")

        if action == "goto":
            if isinstance(payload, dict):
                url = payload.get("url")
                timeout_ms = payload.get("timeout_ms", default_timeout_ms)
                if not url:
                    raise ValueError("goto requires url")
                page.goto(url, timeout=timeout_ms)
            else:
                page.goto(payload)
            continue

        if action == "click":
            if not isinstance(payload, dict):
                raise ValueError("click requires an object selector payload")
            selector, extra = split_selector(payload)
            timeout_ms = extra.get("timeout_ms", default_timeout_ms)
            locator = build_locator(page, selector, extra)
            locator.click(timeout=timeout_ms)
            continue

        if action == "fill":
            if not isinstance(payload, dict):
                raise ValueError("fill requires an object selector payload")
            selector, extra = split_selector(payload)
            value = extra.get("value")
            if value is None:
                raise ValueError("fill requires value")
            timeout_ms = extra.get("timeout_ms", default_timeout_ms)
            locator = build_locator(page, selector, extra)
            locator.fill(str(value), timeout=timeout_ms)
            continue

        if action == "wait_for":
            if not isinstance(payload, dict):
                raise ValueError("wait_for requires an object selector payload")
            selector, extra = split_selector(payload)
            timeout_ms = extra.get("timeout_ms", default_timeout_ms)
            state = extra.get("state", "visible")
            locator = build_locator(page, selector, extra)
            locator.wait_for(state=state, timeout=timeout_ms)
            continue

        if action == "sleep_ms":
            time.sleep(float(payload) / 1000)
            continue

        raise ValueError(f"Unknown action '{action}'")


def open_context(playwright, profile_dir, headless, slow_mo, channel):
    launch_args = {
        "user_data_dir": str(profile_dir),
        "headless": headless,
        "slow_mo": slow_mo,
    }
    if channel:
        launch_args["channel"] = channel
    return playwright.chromium.launch_persistent_context(**launch_args)


def add_shared_flags(parser):
    default_profile = str(Path.cwd() / "autochrome_profile")
    parser.add_argument(
        "--profile",
        default=default_profile,
        help=f"Profile folder (default: {default_profile})",
    )
    parser.add_argument(
        "--channel",
        default=None,
        help="Browser channel (e.g., chrome). Omit to use Playwright Chromium.",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run without a visible browser window.",
    )
    parser.add_argument(
        "--slowmo",
        type=int,
        default=0,
        help="Slow down actions by N ms for visibility.",
    )
    parser.add_argument(
        "--timeout-ms",
        type=int,
        default=DEFAULT_TIMEOUT_MS,
        help=f"Default timeout for actions (ms). Default: {DEFAULT_TIMEOUT_MS}",
    )
    parser.add_argument(
        "--keep-open",
        action="store_true",
        help="Keep the browser open until you press Enter.",
    )


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="AutoChrome 8 - Playwright-based automation runner",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run a JSON flow file")
    run_parser.add_argument("file", help="Path to a JSON flow file")
    add_shared_flags(run_parser)

    test_parser = subparsers.add_parser("test", help="Run a single action line")
    test_parser.add_argument("action", help="Action line, e.g. \"click css=button\"")
    add_shared_flags(test_parser)

    profile_parser = subparsers.add_parser("profile", help="Open a profile window")
    profile_parser.add_argument(
        "--url", default="about:blank", help="Page to open for manual login"
    )
    add_shared_flags(profile_parser)

    args = parser.parse_args(argv)
    profile_dir = normalize_profile_dir(args.profile)
    ensure_dir(profile_dir)

    steps = None
    if args.command == "run":
        steps = load_steps(args.file)
    elif args.command == "test":
        steps = [parse_action_line(args.action)]

    with sync_playwright() as playwright:
        context = open_context(
            playwright,
            profile_dir,
            headless=args.headless,
            slow_mo=args.slowmo,
            channel=args.channel,
        )
        page = context.new_page()

        try:
            if args.command == "profile":
                page.goto(args.url)
                print("Profile window is open. Log in as needed.")
                print("Press Enter to close the window.")
                input()
            else:
                run_steps(page, steps, args.timeout_ms)
                print("Done.")
                if args.keep_open:
                    print("Press Enter to close the window.")
                    input()
        except Exception as exc:
            screenshot = save_error_screenshot(page)
            if screenshot:
                print(f"Error: {exc}. Saved screenshot: {screenshot}")
            else:
                print(f"Error: {exc}.")
            sys.exit(1)
        finally:
            context.close()


if __name__ == "__main__":
    main()
