# A-TAG-FINDER

A-TAG-FINDER is a Python script designed to extract all `<a>` tags along with their `href` attributes from a given webpage. It utilizes the `requests`, `BeautifulSoup`, and `pyfiglet` libraries to fetch the HTML content of the webpage, parse it, and identify the `<a>` tags.

## Features

- Fetches HTML content from a specified URL
- Parses HTML content using BeautifulSoup
- Extracts all `<a>` tags and their `href` attributes
- Displays the extracted `href` attributes

## Prerequisites

- Python 3
- `requests` library (`pip install requests`)
- `BeautifulSoup` library (`pip install beautifulsoup4`)
- `pyfiglet` library (`pip install pyfiglet`)

## Usage

1. Clone the repository:

```
git clone https://github.com/Yamashita012/A-Tag-Finder.git
```

2. Navigate to the cloned directory:

```
cd A-Tag-Finder
```

3. Run the script with a URL as an argument:

```
python3 a_tag_finder.py <URL>
```

Replace `<URL>` with the URL of the webpage you want to analyze.

## Example

```
python3 a_tag_finder.py https://example.com
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## Acknowledgments

- Thanks to the creators of `requests`, `BeautifulSoup`, and `pyfiglet` for their amazing libraries!
- Inspired by the need for a simple tool to extract `<a>` tags from web pages.

Happy scraping! 🕸️
