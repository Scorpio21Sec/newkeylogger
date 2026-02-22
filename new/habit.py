import json
import os
from datetime import datetime, timedelta

# --- CHANGE: Save to AppData/Roaming to avoid permission errors ---
APP_NAME = "HabitTracker"
APPDATA_PATH = os.getenv('APPDATA')
APP_FOLDER = os.path.join(APPDATA_PATH, APP_NAME)
DATA_FILE = os.path.join(APP_FOLDER, "habits_data.json")

# Ensure the folder exists
if not os.path.exists(APP_FOLDER):
    os.makedirs(APP_FOLDER)
# ------------------------------------------------------------------

class HabitManager:
    def __init__(self):
        self.habits = self.load_data()

    def load_data(self):
        # Check if file exists in the new secure location
        if not os.path.exists(DATA_FILE):
            return {}
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.habits, f, indent=4)

    def add_habit(self, habit_name):
        if habit_name and habit_name not in self.habits:
            self.habits[habit_name] = {
                "created_at": datetime.now().strftime("%Y-%m-%d"),
                "history": []
            }
            self.save_data()
            return True
        return False

    def delete_habit(self, habit_name):
        if habit_name in self.habits:
            del self.habits[habit_name]
            self.save_data()

    def toggle_today(self, habit_name):
        today = datetime.now().strftime("%Y-%m-%d")
        if habit_name in self.habits:
            history = self.habits[habit_name]["history"]
            if today in history:
                history.remove(today)
            else:
                history.append(today)
            self.save_data()

    def is_done_today(self, habit_name):
        today = datetime.now().strftime("%Y-%m-%d")
        return today in self.habits.get(habit_name, {}).get("history", [])

    def get_analysis(self, habit_name):
        history = self.habits[habit_name]["history"]
        if not history:
            return {"streak": 0, "total": 0, "last_7_days": 0}

        dates = sorted([datetime.strptime(d, "%Y-%m-%d") for d in history])
        total = len(dates)
        
        streak = 0
        today = datetime.now().date()
        check_date = today
        
        if today not in [d.date() for d in dates]:
            check_date = today - timedelta(days=1)
            
        while check_date in [d.date() for d in dates]:
            streak += 1
            check_date -= timedelta(days=1)

        last_7 = 0
        week_ago = today - timedelta(days=7)
        for d in dates:
            if d.date() > week_ago:
                last_7 += 1

        return {"streak": streak, "total": total, "last_7_days": last_7}