



import requests
from bs4 import BeautifulSoup
import re
import os


SITE_URL = "https://www.selcuksportshdaf3795953b.xyz"   
LINK_PATTERN = r"https?://[^\s'\"]+\.m3u8[^\s'\"]*"  
OUTPUT_FILE = "links.txt"


def fetch_html(url):
    headers = {"User-Agent": "Mozilla/5.0 (compatible)"}
    r = requests.get(url, headers=headers, timeout=15)
    r.raise_for_status()
    return r.text

def extract_links_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True)
    links = set()


    for a in soup.find_all("a", href=True):
        links.add(a["href"])


    for m in re.findall(LINK_PATTERN, text, flags=re.IGNORECASE):
        links.add(m)


    for script in soup.find_all(["script", "source"]):
        if script.string:
            for m in re.findall(LINK_PATTERN, script.string, flags=re.IGNORECASE):
                links.add(m)

    final = set()
    for u in links:
        if u.startswith("//"):
            u = "https:" + u
        if u.startswith("http://") or u.startswith("https://"):
            final.add(u)
    return sorted(final)

def read_existing(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [l.strip() for l in f if l.strip()]

def write_links(path, links):
    with open(path, "w", encoding="utf-8") as f:
        for l in links:
            f.write(l + "\n")

def main():
    print("Fetching:", SITE_URL)
    html = fetch_html(SITE_URL)
    links = extract_links_from_html(html)
    print("Found links:", len(links))

    existing = read_existing(OUTPUT_FILE)
    if links == existing:
        print("No changes. Exiting.")
        return

    write_links(OUTPUT_FILE, links)
    print("Updated", OUTPUT_FILE)

if __name__ == "__main__":
    main()
