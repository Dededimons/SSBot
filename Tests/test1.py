#Search page
import sys
import requests
from bs4 import BeautifulSoup

if len(sys.argv) < 2:
    print("Usage: python test_search_page.py <game name>")
    sys.exit(1)

game_name = ' '.join(sys.argv[1:])
search_url = f"https://steamcharts.com/search/?q={game_name}"
print(f"Searching: {search_url}")

response = requests.get(search_url)
if response.status_code != 200:
    print(f"Failed to load search page, status code: {response.status_code}")
    sys.exit(1)

soup = BeautifulSoup(response.text, 'html.parser')
result = soup.select_one("a[href^='/app/']")
if not result:
    print("No game links found on search page.")
else:
    print("First game link found:")
    print(result)
