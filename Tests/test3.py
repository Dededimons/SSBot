import sys
import requests
from bs4 import BeautifulSoup

def fetch_steam_store_page(app_id):
    url = f"https://store.steampowered.com/app/{app_id}"
    res = requests.get(url)
    if res.status_code != 200:
        print(f"Failed to fetch Steam Store page for app_id {app_id}")
        return None
    return res.text

def print_release_date_sections(html):
    soup = BeautifulSoup(html, 'html.parser')

    print("=== Looking for div.release_date ===")
    release_div = soup.find("div", class_="release_date")
    if release_div:
        print(release_div.prettify())
    else:
        print("No div.release_date found")

    print("\n=== Looking for div.details_block ===")
    detail_blocks = soup.find_all("div", class_="details_block")
    if detail_blocks:
        for i, block in enumerate(detail_blocks):
            print(f"\n--- details_block #{i} ---")
            print(block.prettify())
    else:
        print("No div.details_block found")

    print("\n=== Looking for any <label> or <strong> tags with 'Release Date' text ===")
    labels = soup.find_all(["label", "strong"])
    found = False
    for label in labels:
        if "release date" in label.text.lower():
            print(label.prettify())
            found = True
    if not found:
        print("No label or strong tags with 'Release Date' found")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_release_date.py <app_id>")
        sys.exit(1)

    app_id = sys.argv[1]
    html = fetch_steam_store_page(app_id)
    if html:
        print_release_date_sections(html)
