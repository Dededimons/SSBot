import sys
import requests
from bs4 import BeautifulSoup

def get_app_id(game_name):
    search_url = f"https://steamcharts.com/search/?q={game_name}"
    search_res = requests.get(search_url)
    soup = BeautifulSoup(search_res.text, 'html.parser')
    result = soup.select_one("a[href^='/app/']")
    if not result:
        return None
    return result['href'].split("/")[-1]

def get_current_players(app_id):
    api_url = f"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={app_id}"
    res = requests.get(api_url)
    if res.status_code == 200:
        data = res.json()
        if 'response' in data and data['response'].get('result') == 1:
            return data['response'].get('player_count')
    return None

if len(sys.argv) < 2:
    print("Usage: python script.py <game name>")
    sys.exit(1)

game_name = ' '.join(sys.argv[1:])
app_id = get_app_id(game_name)

if not app_id:
    print("Game not found.")
    sys.exit()

player_count = get_current_players(app_id)
if player_count is not None:
    print(f"Current players for '{game_name}' (app_id {app_id}): {player_count}")
else:
    print("Failed to get current player count from Steam API.")
