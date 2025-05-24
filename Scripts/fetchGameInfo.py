import sys
import requests
from bs4 import BeautifulSoup

def get_app_id(game_name):
    search_url = f"https://steamcharts.com/search/?q={game_name}"
    res = requests.get(search_url)
    if res.status_code != 200:
        return None
    soup = BeautifulSoup(res.text, 'html.parser')
    result = soup.select_one("a[href^='/app/']")
    if not result:
        return None
    return result['href'].split("/")[-1]

def get_current_players(app_id):
    api_url = f"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={app_id}"
    res = requests.get(api_url)
    if res.status_code != 200:
        return None
    data = res.json()
    if 'response' in data and data['response'].get('result') == 1:
        return data['response'].get('player_count')
    return None

def get_release_date(app_id):
    url = f"https://store.steampowered.com/app/{app_id}"
    res = requests.get(url)
    if res.status_code != 200:
        return "N/A"
    soup = BeautifulSoup(res.text, 'html.parser')

    release_date_div = soup.find("div", class_="release_date")
    if not release_date_div:
        return "N/A"

    date_div = release_date_div.find("div", class_="date")  
    if date_div:
        return date_div.text.strip()

    return "N/A"


def get_additional_stats(app_id):
    url = f"https://steamcharts.com/app/{app_id}"
    res = requests.get(url)
    if res.status_code != 200:
        return {}

    soup = BeautifulSoup(res.text, 'html.parser')

    stats = {}

    # All-time peak players
    all_time_peak_div = None
    for div in soup.find_all("div", class_="app-stat"):
        if div.get_text(strip=True).lower().endswith("all-time peak"):
            all_time_peak_div = div
            break
    if all_time_peak_div:
        peak_num = all_time_peak_div.select_one(".num")
        stats['all_time_peak'] = peak_num.text.strip() if peak_num else "N/A"
    else:
        stats['all_time_peak'] = "N/A"

    # Release date from Steam Store page
    stats['release_date'] = get_release_date(app_id)

    return stats

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetchGameInfo.py <game name>")
        sys.exit(1)

    game_name = ' '.join(sys.argv[1:])
    print(f"Fetching info for game: {game_name}")

    app_id = get_app_id(game_name)
    if not app_id:
        print("Game not found.")
        sys.exit(1)

    current_players = get_current_players(app_id)
    additional_stats = get_additional_stats(app_id)

    print(f"App ID: {app_id}")
    print(f"Current players: {current_players if current_players is not None else 'N/A'}")
    print(f"All-time peak players: {additional_stats.get('all_time_peak', 'N/A')}")
    print(f"Release date: {additional_stats.get('release_date', 'N/A')}")
