# A-Tag-Finder

A lightweight Python 3 command-line tool for discovering and extracting hyperlinks (`<a>` tags) from a web page.

A-Tag-Finder retrieves a page's HTML and extracts anchor elements that contain an `href` attribute. It can optionally resolve relative links, remove duplicates, include anchor text, and produce JSON output.

## Features

- Fetches HTTP and HTTPS URLs.
- Extracts `href` values from anchor tags.
- Displays the text associated with each link.
- Optionally converts relative links into absolute URLs.
- Optionally removes duplicate links while preserving their original order.
- Supports JSON output for automation and integration.
- Configurable request timeout and User-Agent.
- Handles common HTTP and network errors.
- Displays an ASCII banner (with a built-in fallback if PyFiglet is unavailable).

## Requirements

- Python 3.8 or newer
- Internet access to reach the target web page
- Python packages listed in `requirements.txt`

## Installation

Clone the repository:

```bash
git clone https://github.com/Yamashita012/A-Tag-Finder.git
cd A-Tag-Finder
```

Create and activate a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

## Usage

```bash
python3 a_tag_finder.py <URL> [options]
```

The URL must use `http://` or `https://`.

### Basic scan

```bash
python3 a_tag_finder.py https://example.com
```

### Resolve relative links

Use `--absolute` to convert relative `href` values into absolute URLs based on the final page URL after redirects:

```bash
python3 a_tag_finder.py https://example.com --absolute
```

### Remove duplicate links

```bash
python3 a_tag_finder.py https://example.com --unique
```

### Include empty `href` attributes

```bash
python3 a_tag_finder.py https://example.com --include-empty
```

### JSON output

```bash
python3 a_tag_finder.py https://example.com --json
```

JSON output includes the requested URL, final URL after redirects, HTTP status code, number of extracted links, each link's `href`, and its anchor text.

### Set a custom timeout and User-Agent

```bash
python3 a_tag_finder.py https://example.com --timeout 30 --user-agent "MyReconTool/1.0"
```

### Combine options

```bash
python3 a_tag_finder.py https://example.com \
  --absolute \
  --unique \
  --timeout 30
```

### Hide the banner

```bash
python3 a_tag_finder.py https://example.com --no-banner
```

## Command-line options

| Option | Description |
|---|---|
| `-h`, `--help` | Show help and exit |
| `-t`, `--timeout` | Request timeout in seconds (default: `15`) |
| `-u`, `--user-agent` | Set the HTTP User-Agent (default: `A-Tag-Finder/2.0`) |
| `-a`, `--absolute` | Resolve relative `href` values to absolute URLs |
| `--unique` | Remove duplicate `href` values, preserving order |
| `--include-empty` | Include anchor tags with an empty `href` |
| `--json` | Print results as JSON |
| `--no-banner` | Suppress the ASCII banner |

## Example output

```text
[+] HTTP 200 | https://example.com
[+] Found 3 link(s)

[001] https://example.com/about
      Text: About

[002] https://example.com/contact
      Text: Contact

[003] https://example.com/login
      Text: Login
```

The exact output depends on the HTML returned by the target server.

## How it works

1. Validates that the supplied URL uses HTTP or HTTPS and includes a hostname.
2. Sends an HTTP GET request to the URL.
3. Follows HTTP redirects and checks the final response status.
4. Parses the returned HTML with Beautiful Soup.
5. Extracts anchor elements with `href` attributes.
6. Applies the requested output options and displays the results.

## Limitations

- A-Tag-Finder parses the HTML response; it does not run JavaScript or render the page in a browser.
- Links added dynamically by client-side JavaScript may not be present in the returned HTML.
- It extracts links from the supplied page only; it does not recursively crawl discovered links.
- It does not determine whether extracted links are reachable or valid.
- Relative links are left unchanged unless `--absolute` is specified.

## Responsible use

Only scan websites and systems that you own or are explicitly authorized to assess. Respect applicable laws, terms of service, rate limits, and engagement scope. A-Tag-Finder makes an HTTP request to the URL supplied by the user.

## Dependencies

Dependencies are maintained in [`requirements.txt`](requirements.txt):

- [Requests](https://requests.readthedocs.io/) — HTTP requests.
- [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) — HTML parsing.
- [PyFiglet](https://github.com/pwaller/pyfiglet) — ASCII banner rendering.

## License

MIT

---

**A-Tag-Finder** — Discover. Enumerate. Analyse.
