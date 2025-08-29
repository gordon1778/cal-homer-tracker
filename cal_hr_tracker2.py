# manual_cal_hr_tracker.py
# Manual script to update Cal Raleigh home run status
import json
from datetime import datetime, timezone

# Configuration - EDIT THESE VALUES MANUALLY
# ==========================================
SEASON_TOTAL_HRS = 18  # Update this with Cal's current season total
HIT_HR_TODAY = False   # Set to True if Cal hit a HR today
BOXSCORE_URL = ""      # Optional: Add MLB.com boxscore URL for today's game
GAME_TIME_UTC = ""     # Optional: Game time in UTC format like "2025-08-29T19:10:00Z"

# Status messages
YES_MESSAGE = "YES 💣🔥"
NO_MESSAGE = "Not yet."

# File to update
STATUS_FILE = "status.json"

def update_status():
    """Update the status.json file with manual data"""
    
    # Get today's date in YYYY-MM-DD format (UTC)
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    
    # Prepare status data
    status_data = {
        "date": today,
        "home_run": HIT_HR_TODAY,
        "status": YES_MESSAGE if HIT_HR_TODAY else NO_MESSAGE,
        "season_total": SEASON_TOTAL_HRS
    }
    
    # Add optional fields if provided
    if BOXSCORE_URL:
        status_data["boxscore"] = BOXSCORE_URL
    
    if GAME_TIME_UTC:
        status_data["game_time_utc"] = GAME_TIME_UTC
    
    # Write to status.json
    with open(STATUS_FILE, 'w') as f:
        json.dump(status_data, f, indent=2)
    
    print("✅ Updated status file:")
    print(json.dumps(status_data, indent=2))
    return status_data

if __name__ == "__main__":
    update_status()
