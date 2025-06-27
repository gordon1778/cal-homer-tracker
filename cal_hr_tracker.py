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

# MLB API endpoint for game logs
gamelog_url = f"https://statsapi.mlb.com/api/v1/people/{PLAYER_ID}/stats?stats=gameLog&season={SEASON}"

# Fetch the game logs
response = requests.get(gamelog_url)
data = response.json()

games = data['stats'][0]['splits']

hit_hr_today = False
boxscore_url = ""

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
        break

# Prepare status file content
status_data = {
    "date": today,
    "home_run": hit_hr_today,
    "status": "YES 💣🔥" if hit_hr_today else "Not yet."
}

# Add boxscore URL if available
if boxscore_url:
    status_data["boxscore"] = boxscore_url

# Write to status.json
with open(STATUS_FILE, 'w') as f:
    json.dump(status_data, f, indent=2)

print("Updated status file:", status_data)
