import json
from collections import defaultdict
from pathlib import Path
from typing import List, Dict, Any, Optional


def export_league_to_json(
    teams: List[Dict[str, Any]],
    regular_season_games: List[Dict[str, Any]],
    playoff_games: List[Dict[str, Any]],
    output_path: Path,
    season_year: Optional[int] = None,
    champion_team: Optional[str] = None,
) -> None:
    """
    Export full league data and stats to a JSON file.

    EXPECTED STRUCTURES
    -------------------
    teams: list of dicts like:
        {
            "name": "Alabama",
            "division": "East",
            "conference": "AFC",  # optional but nice
            ...
        }

    regular_season_games: list of dicts like:
        {
            "week": 1,
            "home": "Alabama",
            "away": "Alaska",
            "home_score": 24,
            "away_score": 17,
            "division_game": True,     # optional
        }

    playoff_games: list of dicts like:
        {
            "round": "Divisional",     # or "Wildcard", "Championship", etc.
            "home": "Alabama",
            "away": "Arizona",
            "home_score": 21,
            "away_score": 14,
            "is_championship": False,  # True only for the final game (optional)
        }

    champion_team:
        If None, and there is a playoff game with is_championship=True, we will
        use the winner of that game as the champion.
    """

    # -----------------------
    # 1. Initialize containers
    # -----------------------
    team_stats = {}
    team_by_name = {t["name"]: t for t in teams}

    for t in teams:
        name = t["name"]
        team_stats[name] = {
            "team_name": name,
            "division": t.get("division"),
            "conference": t.get("conference"),
            "regular_season": {
                "games_played": 0,
                "wins": 0,
                "losses": 0,
                "ties": 0,
                "points_for": 0,
                "points_against": 0,
            },
            "playoffs": {
                "berth": False,
                "games_played": 0,
                "wins": 0,
                "losses": 0,
                "ties": 0,
                "points_for": 0,
                "points_against": 0,
            },
            "titles": {
                "division_champion": False,
                "championships": 0,
            },
        }

    # -----------------------
    # 2. Helper to apply a game
    # -----------------------
    def apply_game(
        game: Dict[str, Any],
        is_playoff: bool = False,
    ) -> None:
        home = game["home"]
        away = game["away"]
        hs = game["home_score"]
        as_ = game["away_score"]

        if home not in team_stats or away not in team_stats:
            # Ignore weird games
            return

        home_rec = team_stats[home]["playoffs" if is_playoff else "regular_season"]
        away_rec = team_stats[away]["playoffs" if is_playoff else "regular_season"]

        # Mark playoff berth if needed
        if is_playoff:
            team_stats[home]["playoffs"]["berth"] = True
            team_stats[away]["playoffs"]["berth"] = True

        # Games played
        home_rec["games_played"] += 1
        away_rec["games_played"] += 1

        # Points for/against
        home_rec["points_for"] += hs
        home_rec["points_against"] += as_
        away_rec["points_for"] += as_
        away_rec["points_against"] += hs

        # W/L/T (supports ties)
        if hs > as_:
            home_rec["wins"] += 1
            away_rec["losses"] += 1
        elif as_ > hs:
            away_rec["wins"] += 1
            home_rec["losses"] += 1
        else:
            # tie
            home_rec["ties"] += 1
            away_rec["ties"] += 1

    # -----------------------
    # 3. Apply all games
    # -----------------------
    for g in regular_season_games:
        apply_game(g, is_playoff=False)

    for g in playoff_games:
        apply_game(g, is_playoff=True)

    # -----------------------
    # 4. Determine division titles
    # -----------------------
    # Group teams by division
    divisions = defaultdict(list)
    for name, stats in team_stats.items():
        div = stats["division"]
        divisions[div].append(name)

    def winning_key(name: str):
        rs = team_stats[name]["regular_season"]
        # basic win pct with ties as half-win; tiebreaker by points diff then name
        games = rs["games_played"]
        if games == 0:
            pct = 0.0
        else:
            pct = (rs["wins"] + 0.5 * rs["ties"]) / games
        point_diff = rs["points_for"] - rs["points_against"]
        # negative name for reverse lex would be silly; just add name as last tiebreak
        return (pct, point_diff, name)

    for div, team_names in divisions.items():
        if not div or not team_names:
            continue
        # pick the best record in this division
        champ = max(team_names, key=winning_key)
        team_stats[champ]["titles"]["division_champion"] = True

    # -----------------------
    # 5. Determine champion
    # -----------------------
    if champion_team is None:
        # Try to infer from a championship game
        champ_game = None
        for g in playoff_games:
            if g.get("is_championship"):
                champ_game = g
                break
        if champ_game:
            hs = champ_game["home_score"]
            as_ = champ_game["away_score"]
            if hs > as_:
                champion_team = champ_game["home"]
            elif as_ > hs:
                champion_team = champ_game["away"]
            else:
                # tie in a championship is weird; ignore
                champion_team = None

    if champion_team and champion_team in team_stats:
        team_stats[champion_team]["titles"]["championships"] += 1

    # -----------------------
    # 6. Build final league JSON structure
    # -----------------------
    league_data = {
        "season_year": season_year,
        "teams": teams,  # raw team metadata
        "teams_stats": team_stats,
        "regular_season_games": regular_season_games,
        "playoff_games": playoff_games,
    }

    # -----------------------
    # 7. Write to disk
    # -----------------------
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(league_data, f, indent=2, sort_keys=True)


# Example usage:
if __name__ == "__main__":
    # You would replace these with your real in-memory objects
    dummy_teams = [
        {"name": "Alabama", "division": "East"},
        {"name": "Alaska", "division": "East"},
        {"name": "Arizona", "division": "West"},
    ]

    dummy_regular = [
        {
            "week": 1,
            "home": "Alabama",
            "away": "Alaska",
            "home_score": 24,
            "away_score": 17,
            "division_game": True,
        },
        {
            "week": 1,
            "home": "Arizona",
            "away": "Alabama",
            "home_score": 10,
            "away_score": 10,
            "division_game": False,
        },
    ]

    dummy_playoffs = [
        {
            "round": "Championship",
            "home": "Alabama",
            "away": "Arizona",
            "home_score": 21,
            "away_score": 14,
            "is_championship": True,
        }
    ]

    export_league_to_json(
        teams=dummy_teams,
        regular_season_games=dummy_regular,
        playoff_games=dummy_playoffs,
        output_path=Path("league_2025.json"),
        season_year=2025,
        # champion_team=None  # let it infer from is_championship game
    )

