#Find ID
import sys
import requests
from bs4 import BeautifulSoup

if len(sys.argv) < 2:
    print("Usage: python test_extract_app_id.py <game name>")
    sys.exit(1)

game_name = ' '.join(sys.argv[1:])
search_url = f"https://steamcharts.com/search/?q={game_name}"

response = requests.get(search_url)
soup = BeautifulSoup(response.text, 'html.parser')
result = soup.select_one("a[href^='/app/']")
if not result:
    print("Game not found.")
else:
    app_id = result['href'].split('/')[-1]
    print(f"Extracted app_id: {app_id}")
