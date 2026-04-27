import json
import os

LEADERBOARD_FILE = "leaderboard.json"
SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "sound": True,
    "car_color": "blue",
    "difficulty": "normal"
}


def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_leaderboard(entries):
    entries.sort(key=lambda x: x["score"], reverse=True)
    entries = entries[:10]
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(entries, f, indent=2)
    return entries


def add_leaderboard_entry(name, score, distance):
    entries = load_leaderboard()
    entries.append({"name": name, "score": score, "distance": distance})
    return save_leaderboard(entries)


def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                s = json.load(f)
                for k, v in DEFAULT_SETTINGS.items():
                    if k not in s:
                        s[k] = v
                return s
        except (json.JSONDecodeError, IOError):
            pass
    return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)