# cal_hr_tracker.py
# This script checks if Cal Raleigh hit a home run today and updates a status file.

import requests
from datetime import datetime, timezone
import json

# Constants
PLAYER_ID = 666969  # Cal Raleigh
SEASON = datetime.now().year
STATUS_FILE = "status.json"

# Get today's date in YYYY-MM-DD format (UTC)
today = datetime.now(timezone.utc).strftime('%Y-%m-%d')

# MLB API endpoints
gamelog_url = f"https://statsapi.mlb.com/api/v1/people/{PLAYER_ID}/stats?stats=gameLog&season={SEASON}"
season_url = f"https://statsapi.mlb.com/api/v1/people/{PLAYER_ID}/stats?stats=season&season={SEASON}"

# Fetch game logs and season totals
response_game = requests.get(gamelog_url)
response_season = requests.get(season_url)
data_game = response_game.json()
data_season = response_season.json()

games = data_game['stats'][0]['splits']
season_stats = data_season['stats'][0]['splits'][0]['stat']

hit_hr_today = False
boxscore_url = ""
game_time_utc = None

# Check if there's a game today and if Cal hit a HR
for game in games:
    game_date = game['date']
    if game_date == today:
        statline = game['stat']
        hr = int(statline.get('homeRuns', 0))
        if hr > 0:
            hit_hr_today = True

        # Try to extract the game ID and build box score URL
        game_info = game.get('game')
        if game_info and 'gamePk' in game_info:
            game_id = game_info['gamePk']
            boxscore_url = f"https://www.mlb.com/gameday/{game_id}"

            # Fetch game detail to get game time
            game_detail_url = f"https://statsapi.mlb.com/api/v1.1/game/{game_id}/feed/live"
            game_detail_response = requests.get(game_detail_url)
            game_detail_data = game_detail_response.json()
            game_time_str = game_detail_data.get('gameData', {}).get('datetime', {}).get('dateTime')
            if game_time_str:
                game_time_utc = game_time_str
        break

# Get season total home runs
try:
    total_hrs = int(season_stats.get('homeRuns', 0))
except (TypeError, ValueError):
    total_hrs = 0

# Prepare status file content
status_data = {
    "date": today,
    "home_run": hit_hr_today,
    "status": "YES 💣🔥" if hit_hr_today else "Not yet.",
    "season_total": total_hrs
}

# Add boxscore URL if available
if boxscore_url:
    status_data["boxscore"] = boxscore_url

# Add game time if available
if game_time_utc:
    status_data["game_time_utc"] = game_time_utc

# Write to status.json
with open(STATUS_FILE, 'w') as f:
    json.dump(status_data, f, indent=2)

print("Updated status file:", status_data)
