#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import sys
import pyfiglet
import re

def create_banner(text):
    ascii_banner = pyfiglet.figlet_format(text)
    print(ascii_banner)
create_banner(" A-TAG-FINDER!! ")


def get_a_tags(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        a_tags = soup.find_all('a')
        return a_tags
    except requests.exceptions.RequestException as e:
        print("Error fetching URL:", e)


def extract_href(content):
    pattern = r'href="([^"]*)"'
    match = re.search(pattern, content)

    if match:
        return match.group(1)
    else:
        return None


url = sys.argv[1]
a_tags = get_a_tags(url)


if a_tags:
    print("[+] Found", len(a_tags), "[A TAGS] on", url, "\n")
    for tag in a_tags:
        x = str(tag)
        href_content = extract_href(x)
        print(f"[*] {href_content}")
else:
    print("[-] No a tags found on", url)
