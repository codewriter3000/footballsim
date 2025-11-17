import json
import ast
from pathlib import Path

from game import play_football_game

TEAMS_DIR = Path(__file__).parent / "teams"


def load_team_ratings(team_name: str) -> dict:
    """
    Load a team's ratings from teams/<team_name>.json.

    Tries JSON first; if that fails, falls back to Python literal (e.g., single quotes).
    """
    path = TEAMS_DIR / f"{team_name}.json"
    text = path.read_text(encoding="utf-8")

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return ast.literal_eval(text)


def get_team(teams, name: str) -> dict:
    for t in teams:
        if t["name"] == name:
            return t
    raise ValueError(f"Team not found: {name}")


def generate_regular_season_schedule(team_objs):
    # use names for schedule
    names = [t["name"] for t in team_objs]
    teams = list(names)
    n = len(teams)
    if n % 2 == 1:
        raise ValueError("Does not support odd # teams yet")

    schedule = []
    for _round_idx in range(n - 1):
        week_games = []
        for i in range(n // 2):
            home = teams[i]
            away = teams[n - 1 - i]
            week_games.append((home, away))
        schedule.append(week_games)
        teams = [teams[0]] + [teams[-1]] + teams[1:-1]
    return schedule


def run_league():
    teams = [
        {"name": "Hunterdon", "wins": 0, "losses": 0, "points_for": 0, "points_against": 0},
        {"name": "Somerset",  "wins": 0, "losses": 0, "points_for": 0, "points_against": 0},
        {"name": "Middlesex", "wins": 0, "losses": 0, "points_for": 0, "points_against": 0},
        {"name": "Mercer",    "wins": 0, "losses": 0, "points_for": 0, "points_against": 0},
        {"name": "Monmouth",  "wins": 0, "losses": 0, "points_for": 0, "points_against": 0},
        {"name": "Ocean",     "wins": 0, "losses": 0, "points_for": 0, "points_against": 0},
    ]

    # Load ratings for each team by name
    team_ratings = {t["name"]: load_team_ratings(t["name"]) for t in teams}

    schedule = generate_regular_season_schedule(teams)

    for week_num, games in enumerate(schedule, start=1):
        print(f"Week {week_num}")
        for home_name, away_name in games:
            home_team_obj = get_team(teams, home_name)
            away_team_obj = get_team(teams, away_name)

            # Simulate game: Team 1 = home, Team 2 = away
            result = play_football_game(
                team_ratings[home_name],
                team_ratings[away_name],
            )

            home_points = result["Team 1"]
            away_points = result["Team 2"]

            print(f"  {home_name} {home_points} - {away_points} {away_name}")

            # --- UPDATE STATS HERE ---

            # Points for / against
            home_team_obj["points_for"]     += home_points
            home_team_obj["points_against"] += away_points
            away_team_obj["points_for"]     += away_points
            away_team_obj["points_against"] += home_points

            # Wins / losses (ties: no change)
            if home_points > away_points:
                home_team_obj["wins"]  += 1
                away_team_obj["losses"] += 1
            elif away_points > home_points:
                away_team_obj["wins"]  += 1
                home_team_obj["losses"] += 1
            # if equal, treat as a tie (no wins/losses updated)

        print()  # blank line between weeks

    # Final standings
    print("Final Standings")
    for t in sorted(teams, key=lambda x: (-x["wins"], x["losses"], -(x["points_for"] - x["points_against"]))):
        diff = t["points_for"] - t["points_against"]
        print(
            f"{t['name']}: {t['wins']}-{t['losses']}  "
            f"PF={t['points_for']}  PA={t['points_against']}  DIFF={diff}"
        )


if __name__ == "__main__":
    run_league()

