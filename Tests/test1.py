#Search page n iD
import sys
import requests
from bs4 import BeautifulSoup

if len(sys.argv) < 2:
    print("Usage: python test_steamcharts_search.py <game name>")
    sys.exit(1)

game_name = ' '.join(sys.argv[1:])
search_url = f"https://steamcharts.com/search/?q={game_name}"
print(f"Searching SteamCharts with URL: {search_url}")

response = requests.get(search_url)
print(f"Status code: {response.status_code}")
if response.status_code != 200:
    print("Failed to get search results.")
    sys.exit(1)

soup = BeautifulSoup(response.text, 'html.parser')
result = soup.select_one("a[href^='/app/']")

if not result:
    print("No game found.")
else:
    print("First game link found:")
    print(result)  # Prints full <a> tag
    app_id = result['href'].split('/')[-1]
    print(f"Extracted app_id: {app_id}")
