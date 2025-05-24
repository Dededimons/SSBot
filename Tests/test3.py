#Player count
import sys
import requests
from bs4 import BeautifulSoup

if len(sys.argv) < 2:
    print("Usage: python test_fetch_player_count.py <app_id>")
    sys.exit(1)

app_id = sys.argv[1]
data_url = f"https://steamcharts.com/app/{app_id}"
response = requests.get(data_url)
print(f"Request status: {response.status_code}")
if response.status_code != 200:
    print("Failed to load app page.")
    sys.exit(1)

soup = BeautifulSoup(response.text, 'html.parser')

app_stats = soup.find_all("div", class_="app-stat")
print(f"Found {len(app_stats)} 'app-stat' divs.")

for i, stat in enumerate(app_stats):
    print(f"\nApp-stat block #{i}:")
    print(stat.prettify())

player_elem = soup.select_one(".app-stat .num")
if player_elem:
    print(f"\nExtracted player count: {player_elem.text.strip()}")
else:
    print("\nPlayer count not found using '.app-stat .num' selector.")

    # Print first 500 chars of full page for manual inspection
    print("\nFirst 500 characters of page HTML:")
    print(response.text[:500])
