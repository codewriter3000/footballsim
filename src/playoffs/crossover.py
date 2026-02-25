import random
from typing import Dict, List

from ..game_logic.game import play_football_game

# Pseudo-conference mappings for crossover games
EAST_DIVISIONS = {
    "New England",
    "Mid-Atlantic",
    "Chesapeake",
    "Southeast",
    "Southwest",
}
WEST_DIVISIONS = {
    "Great Lakes",
    "Appalachia",
    "Plains",
    "Rocky",
    "Pacific",
}

def simulate_crossover_games(
    crossover_teams: List[Dict],
    team_ratings: Dict[str, Dict],
    crossover_games: List[Dict[str, any]],
    target_games: int = 10,
) -> None:
    """
    Schedule and simulate 'conference crossover' games for teams that did not
    make the playoffs.

    Every non-playoff team is *guaranteed* up to `target_games` total games
    (regular season + crossover). We infer current games from wins/losses/ties.

    We fake two conferences by grouping divisions:
      - East Conf:  New England, Mid-Atlantic, Chesapeake, Southeast, Southwest
      - West Conf:  Great Lakes, Appalachia, Plains, Rocky, Pacific

    Only games between East/West are scheduled here.
    """
    if not crossover_teams:
        return

    print("\n=== CROSSOVERS ===\n")

    team_state: Dict[str, Dict] = {}
    already_played = set()  # track crossover matchups we create here

    for t in crossover_teams:
        name = t["name"]
        games_played = t["wins"] + t["losses"] + t["ties"]
        division = t.get("division", "")

        if division in EAST_DIVISIONS:
            conference = "East"
        elif division in WEST_DIVISIONS:
            conference = "West"
        else:
            conference = "Ind"

        team_state[name] = {
            "team": t,  # reference to original dict
            "name": name,
            "division": division,
            "conference": conference,
            "games_played": games_played,
            "needed": max(0, target_games - games_played),
        }

    round_num = 1

    while True:
        needing = [ts for ts in team_state.values() if ts["needed"] > 0]

        if len(needing) < 2:
            break

        needing.sort(key=lambda ts: (ts["games_played"], ts["name"]))

        print(f"--- Crossover Week {round_num} ---")
        used_this_round = set()
        made_pair = False

        for ts in needing:
            name = ts["name"]
            if ts["needed"] <= 0 or name in used_this_round:
                continue

            conf = ts["conference"]
            if conf not in ("East", "West"):
                continue

            desired_opponent_conf = "West" if conf == "East" else "East"

            opponent_ts = None
            # Try to find a fresh cross-conference opponent
            for cand in needing:
                cname = cand["name"]
                if (
                    cname == name
                    or cand["needed"] <= 0
                    or cname in used_this_round
                    or cand["conference"] != desired_opponent_conf
                ):
                    continue

                matchup_key = frozenset((name, cname))
                if matchup_key in already_played:
                    continue

                opponent_ts = cand
                break

            # If no fresh opponent, allow a repeat if necessary
            if opponent_ts is None:
                for cand in needing:
                    cname = cand["name"]
                    if (
                        cname == name
                        or cand["needed"] <= 0
                        or cname in used_this_round
                        or cand["conference"] != desired_opponent_conf
                    ):
                        continue
                    opponent_ts = cand
                    break

            if opponent_ts is None:
                continue

            home_name, away_name = name, opponent_ts["name"]
            if random.choice((True, False)):
                home_name, away_name = away_name, home_name

            result = play_football_game(
                team_ratings[home_name],
                team_ratings[away_name],
            )
            home_points = result["Team 1"]
            away_points = result["Team 2"]

            print(f"  {home_name} {home_points} - {away_points} {away_name}")

            crossover_games.append({
                "round": f"C{round_num}",
                "home": home_name,
                "away": away_name,
                "home_score": home_points,
                "away_score": away_points,
                "division_game": False, # cross-conference by design
            })

            home_team = team_state[home_name]["team"]
            away_team = team_state[away_name]["team"]

            home_team["points_for"] += home_points
            home_team["points_against"] += away_points
            away_team["points_for"] += away_points
            away_team["points_against"] += home_points

            if home_points > away_points:
                home_team["wins"] += 1
                away_team["losses"] += 1
            elif away_points > home_points:
                away_team["wins"] += 1
                home_team["losses"] += 1
            else:
                home_team["ties"] += 1
                away_team["ties"] += 1

            for n in (home_name, away_name):
                team_state[n]["games_played"] += 1
                if team_state[n]["needed"] > 0:
                    team_state[n]["needed"] -= 1

            used_this_round.add(home_name)
            used_this_round.add(away_name)
            already_played.add(frozenset((home_name, away_name)))
            made_pair = True

        print()

        if not made_pair:
            # No pairings possible this week; avoid infinite loop
            break

        round_num += 1

    print("Crossover scheduling complete.\n")