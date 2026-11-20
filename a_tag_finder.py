#!/usr/bin/env python3

"""
A-Tag-Finder: enumerate and extract hyperlinks from a web page.

Dependencies:
    python3 -m pip install requests beautifulsoup4

Optional ASCII banner:
    python3 -m pip install pyfiglet
"""

import argparse
import json
import sys
from urllib.parse import urljoin, urlparse
import pyfiglet

import requests
from bs4 import BeautifulSoup

BANNER = pyfiglet.figlet_format("A-Tag-Finder", font="slant")
print(BANNER)

def print_banner(use_pyfiglet=True):
    """Print a large banner, falling back to built-in ASCII art."""
    if use_pyfiglet:
        try:
            import pyfiglet
            print(pyfiglet.figlet_format("A-TAG-FINDER", font="slant"))
            return
        except (ImportError, Exception):
            pass
    print(BANNER)


def validate_url(value):
    """argparse validator: accept only HTTP and HTTPS URLs with a hostname."""
    parsed = urlparse(value)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise argparse.ArgumentTypeError(
            "URL must start with http:// or https:// and include a hostname"
        )
    return value


def fetch_page(url, timeout, user_agent):
    """Fetch a page and return its HTML and final response URL."""
    headers = {"User-Agent": user_agent}
    response = requests.get(
        url,
        headers=headers,
        timeout=timeout,
        allow_redirects=True,
    )
    response.raise_for_status()
    return response.text, response.url, response.status_code


def extract_links(html, page_url, absolute=False, include_empty=False, unique=False):
    """Extract href attributes from anchor tags."""
    soup = BeautifulSoup(html, "html.parser")
    results = []

    for anchor in soup.find_all("a", href=True):
        href = anchor.get("href", "").strip()

        if not href and not include_empty:
            continue

        link = urljoin(page_url, href) if absolute and href else href
        if not link and not include_empty:
            continue

        results.append({
            "href": link,
            "text": " ".join(anchor.get_text(" ", strip=True).split()),
        })

    if unique:
        seen = set()
        deduplicated = []
        for item in results:
            if item["href"] not in seen:
                seen.add(item["href"])
                deduplicated.append(item)
        results = deduplicated

    return results


def build_parser():
    parser = argparse.ArgumentParser(
        prog="a_tag_finder.py",
        description="Discover and extract <a> tag links from a web page.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("url", type=validate_url, help="Target HTTP(S) URL")
    parser.add_argument(
        "-t", "--timeout", type=float, default=15,
        help="Request timeout in seconds",
    )
    parser.add_argument(
        "-u", "--user-agent", default="A-Tag-Finder/2.0",
        help="HTTP User-Agent header",
    )
    parser.add_argument(
        "-a", "--absolute", action="store_true",
        help="Resolve relative href values to absolute URLs",
    )
    parser.add_argument(
        "--unique", action="store_true",
        help="Remove duplicate href values while preserving order",
    )
    parser.add_argument(
        "--include-empty", action="store_true",
        help="Include anchor tags with an empty href attribute",
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Print results as JSON",
    )
    parser.add_argument(
        "--no-banner", action="store_true",
        help="Do not display the ASCII banner",
    )
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero")

    if not args.no_banner and not args.json:
        print_banner()

    try:
        html, final_url, status_code = fetch_page(
            args.url, args.timeout, args.user_agent
        )
        links = extract_links(
            html,
            final_url,
            absolute=args.absolute,
            include_empty=args.include_empty,
            unique=args.unique,
        )
    except requests.exceptions.Timeout:
        print("[!] Request timed out. Increase --timeout and try again.", file=sys.stderr)
        return 1
    except requests.exceptions.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else "unknown"
        print(f"[!] HTTP error: {status} ({exc})", file=sys.stderr)
        return 1
    except requests.exceptions.RequestException as exc:
        print(f"[!] Network error: {exc}", file=sys.stderr)
        return 1
    except (ValueError, UnicodeError) as exc:
        print(f"[!] Could not process response: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps({
            "requested_url": args.url,
            "final_url": final_url,
            "status_code": status_code,
            "count": len(links),
            "links": links,
        }, indent=2, ensure_ascii=False))
        return 0

    print(f"[+] HTTP {status_code} | {final_url}")
    print(f"[+] Found {len(links)} link(s)\n")

    if not links:
        print("[-] No matching <a href='...'> elements found.")
        return 0

    for index, item in enumerate(links, start=1):
        print(f"[{index:03}] {item['href']}")
        if item["text"]:
            print(f"      Text: {item['text']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
