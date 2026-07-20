#!/usr/bin/env python3
"""Check that external source URLs cited in docs/ are still reachable.

This tool is deliberately NOT part of `xtask check`. It requires network access
and depends on third-party availability, so it must never gate the offline
repository validation path. Run it manually, or on a schedule, to catch cited
specifications that have moved or been withdrawn.

Motivation: on 2026-07-20 every chapter of the extensions-enterprise book cited
`https://wicg.github.io/webextensions/`, which had begun returning HTTP 404
after the WebExtensions Community Group specification moved. All ninety
validators passed, because the repository's link checks resolve internal
repository paths and never touch external URLs.

Exit status is 1 when a URL is confirmed dead, 0 otherwise. Ambiguous results
(timeouts, bot-blocking 403s, rate limiting) are reported but do not fail the
run: they are access conditions, not evidence that a source is gone.

Usage:
    python3 -B tools/check_external_links.py
    python3 -B tools/check_external_links.py --timeout 15 --workers 8
    python3 -B tools/check_external_links.py --path docs/security-engine
"""

from __future__ import annotations

import argparse
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

URL_PATTERN = re.compile(r"https?://[^\s<>\)\]\"'`]+")

# Inline-code spans and fenced blocks are stripped before extraction. A URL
# written as `https://example.invalid/` is being referred to as a string --
# typically to record that it moved or died -- not cited as a live source.
# Citing prose must use a bare URL or a Markdown link to be checked.
CODE_FENCE = re.compile(r"```.*?```", re.S)
INLINE_CODE = re.compile(r"`[^`]*`")

# Markdown link target, allowing one level of balanced parentheses inside the
# URL so selector-style documentation links survive extraction intact.
MD_LINK = re.compile(r"\]\((https?://(?:[^()\s]|\([^()\s]*\))+)\)")

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)

# Hosts that reliably refuse automated requests on live pages. A non-2xx from
# these is not evidence of absence, so they are reported as ambiguous.
BOT_BLOCKING_HOSTS = (
    "dl.acm.org",
    "doi.org",
    "link.springer.com",
    "ieeexplore.ieee.org",
    "sciencedirect.com",
    "usenix.org",
    # crates.io serves a single-page app and returns 404 to plain GETs for
    # crates that exist; https://crates.io/api/v1/crates/<name> returns 200.
    "crates.io",
)

DEAD_STATUSES = {404, 410}


def collect_urls(search_path: Path) -> dict[str, list[str]]:
    """Map each external URL to the repo-relative files citing it."""
    citations: dict[str, list[str]] = {}
    for path in sorted(search_path.rglob("*.md")):
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        text = path.read_text(encoding="utf-8", errors="replace")
        text = CODE_FENCE.sub(" ", text)
        text = INLINE_CODE.sub(" ", text)

        found: set[str] = set()

        # Markdown link targets first. Some real URLs contain parentheses --
        # Apple selector docs such as `...requirement(_:_:)` are the common
        # case -- so a bare-URL regex that stops at the first ')' truncates
        # them into 404s. Consume one level of balanced parentheses here.
        for match in MD_LINK.finditer(text):
            found.add(match.group(1).rstrip(".,;:"))

        # Then bare URLs, skipping any already captured as a link target.
        for match in URL_PATTERN.finditer(text):
            url = match.group(0).rstrip(".,;:")
            if not any(url in seen for seen in found):
                found.add(url)

        for url in found:
            citations.setdefault(url, []).append(rel)
    return citations


def probe(url: str, timeout: int) -> tuple[str, int | None, str]:
    """Return (verdict, status, detail) where verdict is ok/dead/ambiguous."""
    request = urllib.request.Request(
        url, method="GET", headers={"User-Agent": USER_AGENT}
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return "ok", response.status, ""
    except urllib.error.HTTPError as error:
        if error.code in DEAD_STATUSES:
            if any(host in url for host in BOT_BLOCKING_HOSTS):
                return "ambiguous", error.code, "bot-blocking host"
            return "dead", error.code, error.reason or ""
        return "ambiguous", error.code, error.reason or ""
    except Exception as error:  # noqa: BLE001 - network failures are varied
        return "ambiguous", None, f"{type(error).__name__}: {error}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", default="docs", help="directory to scan")
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()

    search_path = (ROOT / args.path).resolve()
    if not search_path.is_dir():
        print(f"external-link check failed: {args.path} is not a directory", file=sys.stderr)
        return 1

    citations = collect_urls(search_path)
    urls = sorted(citations)
    print(f"checking {len(urls)} distinct external URLs under {args.path}/ ...")

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(lambda u: (u, *probe(u, args.timeout)), urls))

    dead = [r for r in results if r[1] == "dead"]
    ambiguous = [r for r in results if r[1] == "ambiguous"]

    if ambiguous:
        print(f"\n{len(ambiguous)} URL(s) could not be confirmed (not treated as failures):")
        for url, _verdict, status, detail in ambiguous:
            print(f"  [{status or '---'}] {url}  {detail}")

    if dead:
        print(f"\n{len(dead)} URL(s) are confirmed dead:", file=sys.stderr)
        for url, _verdict, status, detail in dead:
            print(f"  [{status}] {url}  {detail}", file=sys.stderr)
            for citing in citations[url]:
                print(f"        cited by {citing}", file=sys.stderr)
        print(
            "\nexternal-link check failed: replace or repair the URLs above, and "
            "record the move in the owning document.",
            file=sys.stderr,
        )
        return 1

    print(
        f"\nexternal-link check passed: {len(urls)} URLs, "
        f"{len(dead)} dead, {len(ambiguous)} unconfirmed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
