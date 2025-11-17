import json
import ast
import random
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
    """
    Generate a schedule with:
      - All divisional opponents (single round-robin within division)
      - 2 non-division games per team (if multiple divisions exist)

    Returns: list of weeks, where each week is a list of (home, away) tuples.
    """
    # Map names to divisions and group by division
    divisions: dict[str, list[str]] = {}
    team_to_div: dict[str, str] = {}

    for t in team_objs:
        name = t["name"]
        div = t.get("division", "DIV1")
        team_to_div[name] = div
        divisions.setdefault(div, []).append(name)

    team_names = [t["name"] for t in team_objs]

    # --- 1. Divisional games (each pair in the same division plays once) ---
    all_games = []
    game_keys = set()  # frozenset({team1, team2}) to avoid duplicates

    for div, names in divisions.items():
        # optional sanity check: 5–6 teams per division
        # if not (5 <= len(names) <= 6):
        #     print(f"Warning: division {div} has {len(names)} teams (expected 5–6).")

        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                a, b = names[i], names[j]
                # Randomize home/away
                if random.choice((True, False)):
                    game = (a, b)
                else:
                    game = (b, a)
                all_games.append(game)
                game_keys.add(frozenset((a, b)))

    # --- 2. Non-division games: aim for 2 per team (if possible) ---
    cross_needed = {name: 2 for name in team_names}

    if len(divisions) > 1:
        candidate_pairs = []
        for i in range(len(team_names)):
            for j in range(i + 1, len(team_names)):
                a, b = team_names[i], team_names[j]
                if team_to_div[a] != team_to_div[b]:
                    candidate_pairs.append((a, b))

        random.shuffle(candidate_pairs)

        for a, b in candidate_pairs:
            if cross_needed[a] <= 0 or cross_needed[b] <= 0:
                continue

            key = frozenset((a, b))
            if key in game_keys:
                continue  # already scheduled somehow (safety)

            # Randomize home/away
            if random.choice((True, False)):
                game = (a, b)
            else:
                game = (b, a)

            all_games.append(game)
            game_keys.add(key)
            cross_needed[a] -= 1
            cross_needed[b] -= 1

        # If some teams still have cross_needed > 0 here, it means the structure
        # made it impossible to give everyone exactly 2 non-division games.
        # They will just have fewer cross-division games.

    # --- 3. Turn flat game list into weeks (each team plays at most once per week) ---
    random.shuffle(all_games)
    remaining = all_games[:]
    schedule = []

    while remaining:
        week_games = []
        used_teams = set()
        new_remaining = []

        for home, away in remaining:
            if home in used_teams or away in used_teams:
                new_remaining.append((home, away))
            else:
                week_games.append((home, away))
                used_teams.add(home)
                used_teams.add(away)

        schedule.append(week_games)
        remaining = new_remaining

    return schedule


def run_league():
    # Add divisions; this setup can be expanded to multiple 5–6 team divisions.
    # For now, all your existing teams are in one division called "Atlantic".
    teams = [
        {"name": "New Jersey",      "division": "Atlantic", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0},
        {"name": "Pennsylvania",    "division": "Atlantic", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0},
        {"name": "Delaware",        "division": "Atlantic", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0},
        {"name": "Maryland",        "division": "Atlantic", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0},
        {"name": "Virginia",        "division": "Atlantic", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0},
        {"name": "New York",        "division": "Atlantic", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0},
        {"name": "Connecticut",     "division": "New England", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0},
        {"name": "Rhode Island",    "division": "New England", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0},
        {"name": "Massachusetts",     "division": "New England", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0},
        {"name": "Vermont",     "division": "New England", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0},
        {"name": "New Hampshire",     "division": "New England", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0},
        {"name": "Maine",     "division": "New England", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0},
        {"name": "Louisiana", "division": "Old South", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "South Carolina", "division": "Old South", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "Georgia", "division": "Old South", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "Florida", "division": "Old South", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "Alabama", "division": "Old South", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "Mississippi", "division": "Old South", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "Tennessee", "division": "Appalachian", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "Kentucky", "division": "Appalachian", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "West Virginia", "division": "Appalachian", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "North Carolina", "division": "Appalachian", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "Arkansas", "division": "Appalachian", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "Texas", "division": "Southwest", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "New Mexico", "division": "Southwest", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "Arizona", "division": "Southwest", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "Oklahoma", "division": "Southwest", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "Nevada", "division": "Southwest", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "California", "division": "Pacific", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "Oregon", "division": "Pacific", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "Washington", "division": "Pacific", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "Alaska", "division": "Pacific", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "Hawaii", "division": "Pacific", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "Idaho", "division": "Rockies", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "Wyoming", "division": "Rockies", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "Montana", "division": "Rockies", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "Utah", "division": "Rockies", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "Colorado", "division": "Rockies", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "North Dakota", "division": "Great Plains", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "South Dakota", "division": "Great Plains", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "Nebraska", "division": "Great Plains", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "Kansas", "division": "Great Plains", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "Missouri", "division": "Great Plains", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "Iowa", "division": "Great Plains", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "Ohio", "division": "Midwest", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "Michigan", "division": "Midwest", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "Wisconsin", "division": "Midwest", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "Minnesota", "division": "Midwest", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "Indiana", "division": "Midwest", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},
        {"name": "Illinois", "division": "Midwest", "wins": 0, "losses": 0, "ties": 0, "points_for": 0, "points_against": 0},


        # When you add more teams, give them a division name too, e.g. "Coastal".
        # The scheduler will then create divisional + 2 cross-division games.
    ]

    # Load ratings for each team by name
    team_ratings = {t["name"]: load_team_ratings(t["name"]) for t in teams}

    schedule = generate_regular_season_schedule(team_objs=teams)

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

            # Points for / against
            home_team_obj["points_for"]     += home_points
            home_team_obj["points_against"] += away_points
            away_team_obj["points_for"]     += away_points
            away_team_obj["points_against"] += home_points

            # Wins / losses / ties
            if home_points > away_points:
                home_team_obj["wins"]  += 1
                away_team_obj["losses"] += 1
            elif away_points > home_points:
                away_team_obj["wins"]  += 1
                home_team_obj["losses"] += 1
            else:
                home_team_obj["ties"]  += 1
                away_team_obj["ties"]  += 1

        print()  # blank line between weeks

    # Final standings
    print("Final Standings")

    def standings_key(t):
        diff = t["points_for"] - t["points_against"]
        # Wins desc, ties desc, losses asc, point diff desc
        return (-t["wins"], -t["ties"], t["losses"], -diff)

    for t in sorted(teams, key=standings_key):
        diff = t["points_for"] - t["points_against"]
        print(
            f"{t['name']} ({t['division']}): "
            f"{t['wins']}-{t['losses']}-{t['ties']}  "
            f"PF={t['points_for']}  PA={t['points_against']}  DIFF={diff}"
        )


if __name__ == "__main__":
    run_league()

