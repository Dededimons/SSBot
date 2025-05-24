#Find Player count
import sys
import requests

if len(sys.argv) < 2:
    print("Usage: python test_steam_api_player_count.py <app_id>")
    sys.exit(1)

app_id = sys.argv[1]
api_url = f"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={app_id}"
print(f"Requesting Steam API: {api_url}")

response = requests.get(api_url)
print(f"Status code: {response.status_code}")
if response.status_code != 200:
    print("Failed to get data from Steam API.")
    sys.exit(1)

data = response.json()
print("Raw JSON response:")
print(data)

if 'response' in data and data['response'].get('result') == 1:
    player_count = data['response'].get('player_count')
    print(f"Current player count: {player_count}")
else:
    print("No valid player count found in response.")
