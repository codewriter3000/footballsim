import json
import ast
import random
from pathlib import Path

TEAMS_DIR = Path(__file__).parent / "teams"


def load_team_file(path: Path):
    """
    Load a team's data from a file.

    Tries JSON first; if that fails, falls back to Python literal (e.g., single quotes).
    Returns (data, is_json) so we know how it was parsed (if you ever care).
    """
    text = path.read_text(encoding="utf-8")

    try:
        data = json.loads(text)
        return data, True
    except json.JSONDecodeError:
        data = ast.literal_eval(text)
        return data, False


def clamp_rating(value: float) -> int:
    """
    Clamp rating to be between 50 and 99 inclusive and return as int.
    """
    if value < 50:
        return 50
    if value > 99:
        return 99
    return int(round(value))


def adjust_rating(value):
    """
    If value is numeric, adjust it by a random int in [-5, 5] and clamp to [50, 99].
    Otherwise, return it unchanged.
    """
    if isinstance(value, (int, float)):
        delta = random.randint(-5, 5)
        new_value = value + delta
        return clamp_rating(new_value)
    return value


def adjust_structure(obj):
    """
    Recursively walk the data structure and apply adjust_rating to every numeric value.
    Works on nested dicts/lists.
    """
    if isinstance(obj, dict):
        return {k: adjust_structure(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [adjust_structure(v) for v in obj]
    else:
        # Base case: not a container; maybe a rating
        return adjust_rating(obj)


def save_team_file(path: Path, data):
    """
    Save updated team data back to disk as JSON.
    Your existing loader can still read this (it tries JSON first).
    """
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)


def run_offseason():
    """
    Run the offseason adjustment over every team file in TEAMS_DIR.
    """
    if not TEAMS_DIR.exists():
        raise FileNotFoundError(f"Teams directory not found: {TEAMS_DIR}")

    for path in TEAMS_DIR.glob("*.json"):
        print(f"Processing {path.name}...")
        data, _ = load_team_file(path)
        updated = adjust_structure(data)
        save_team_file(path, updated)

    print("Offseason adjustments complete.")


if __name__ == "__main__":
    run_offseason()

