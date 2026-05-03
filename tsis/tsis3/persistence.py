"""
persistence.py – Save and load leaderboard and settings to/from JSON files.
"""

import json
import os

LEADERBOARD_FILE = "leaderboard.json"
SETTINGS_FILE    = "settings.json"

# ── Default settings ──────────────────────────────────────────────────────────

DEFAULT_SETTINGS = {
    "sound":      True,
    "car_color":  "red",       # "red" | "blue" | "green" | "yellow"
    "difficulty": "normal",    # "easy" | "normal" | "hard"
}

# ── Leaderboard ───────────────────────────────────────────────────────────────

def load_leaderboard():
    """Return the top-10 leaderboard list, or an empty list if the file doesn't exist."""
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            data = json.load(f)
        # Each entry: {"name": str, "score": int, "distance": int, "coins": int}
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError):
        return []


def save_leaderboard(entries):
    """
    Persist the leaderboard.  `entries` is a list of dicts.
    Keeps only the top 10, sorted by score descending.
    """
    sorted_entries = sorted(entries, key=lambda e: e.get("score", 0), reverse=True)
    top10 = sorted_entries[:10]
    try:
        with open(LEADERBOARD_FILE, "w") as f:
            json.dump(top10, f, indent=2)
    except IOError as exc:
        print(f"[persistence] Could not save leaderboard: {exc}")
    return top10


def add_leaderboard_entry(name, score, distance, coins):
    """
    Insert a new result and re-save.
    Returns the updated top-10 list.
    """
    entries = load_leaderboard()
    entries.append({
        "name":     name,
        "score":    score,
        "distance": distance,
        "coins":    coins,
    })
    return save_leaderboard(entries)


# ── Settings ──────────────────────────────────────────────────────────────────

def load_settings():
    """Return saved settings dict, falling back to defaults for missing keys."""
    if not os.path.exists(SETTINGS_FILE):
        return dict(DEFAULT_SETTINGS)
    try:
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)
        # Fill in any keys that are missing (e.g. after an app update)
        for k, v in DEFAULT_SETTINGS.items():
            data.setdefault(k, v)
        return data
    except (json.JSONDecodeError, IOError):
        return dict(DEFAULT_SETTINGS)


def save_settings(settings):
    """Persist the settings dict to disk."""
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=2)
    except IOError as exc:
        print(f"[persistence] Could not save settings: {exc}")