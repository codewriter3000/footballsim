import json
import ast
import random
from pathlib import Path
from typing import Dict, List, Tuple, Iterable, Any

from game import play_football_game
from records import export_league_to_json

SEASON_YEAR = 2025
OUTPUT_JSON = Path(__file__).parent / f"league_{SEASON_YEAR}.json"
TEAMS_DIR = Path(__file__).parent / "teams"

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


def load_team_ratings(team_name: str) -> Dict:
    """
    Load a team's ratings from teams/<team_name>.json.

    Tries JSON first; if that fails, falls back to Python literal (e.g., single quotes).
    """
    path = TEAMS_DIR / f"{team_name}.json"

    if not path.exists():
        raise FileNotFoundError(f"Ratings file not found for team '{team_name}': {path}")

    text = path.read_text(encoding="utf-8")

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Fallback for non-strict JSON (single quotes, etc.)
        return ast.literal_eval(text)


def get_team(teams: Iterable[Dict], name: str) -> Dict:
    for t in teams:
        if t["name"] == name:
            return t
    raise ValueError(f"Team not found: {name}")


def generate_regular_season_schedule(team_objs: List[Dict]) -> List[List[Tuple[str, str]]]:
    """
    Generate a schedule with:
      - All divisional opponents (single round-robin within division)
      - 2 non-division games per team via pairing
      - 1 additional non-division game scheduled on a shared bye week
        (when structure allows)

    Returns: list of weeks, where each week is a list of (home, away) tuples.
    """
    divisions: Dict[str, List[str]] = {}
    team_to_div: Dict[str, str] = {}

    for t in team_objs:
        name = t["name"]
        div = t.get("division", "DIV1")
        team_to_div[name] = div
        divisions.setdefault(div, []).append(name)

    team_names = [t["name"] for t in team_objs]

    # --- 1. Divisional games ---
    all_games: List[Tuple[str, str]] = []
    game_keys = set()  # frozenset({team1, team2}) to avoid duplicates

    for names in divisions.values():
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                a, b = names[i], names[j]
                # Randomize home/away
                home, away = (a, b) if random.choice((True, False)) else (b, a)
                all_games.append((home, away))
                game_keys.add(frozenset((a, b)))

    # --- 2. Non-division games: aim for 2 per team via normal pairing ---
    cross_needed = {name: 2 for name in team_names}

    if len(divisions) > 1:
        candidate_pairs: List[Tuple[str, str]] = []
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
                continue  # already scheduled (safety)

            home, away = (a, b) if random.choice((True, False)) else (b, a)
            all_games.append((home, away))
            game_keys.add(key)
            cross_needed[a] -= 1
            cross_needed[b] -= 1
        # Some teams may get fewer than 2 if structure prevents perfect pairing.

    # --- 3. Pack games into weeks (each team at most once per week) ---
    random.shuffle(all_games)
    remaining = all_games[:]
    schedule: List[List[Tuple[str, str]]] = []

    while remaining:
        week_games: List[Tuple[str, str]] = []
        used_teams = set()
        new_remaining: List[Tuple[str, str]] = []

        for home, away in remaining:
            if home in used_teams or away in used_teams:
                new_remaining.append((home, away))
            else:
                week_games.append((home, away))
                used_teams.add(home)
                used_teams.add(away)

        schedule.append(week_games)
        remaining = new_remaining

    # --- 4. Compute bye weeks for each team ---
    num_weeks = len(schedule)
    bye_weeks = {name: set(range(num_weeks)) for name in team_names}

    for week_idx, games in enumerate(schedule):
        for home, away in games:
            bye_weeks[home].discard(week_idx)
            bye_weeks[away].discard(week_idx)

    # --- 5. Use shared bye weeks to add a 3rd non-division game ---
    extra_needed = {name: 1 for name in team_names}

    extra_pairs: List[Tuple[str, str]] = []
    for i in range(len(team_names)):
        for j in range(i + 1, len(team_names)):
            a, b = team_names[i], team_names[j]
            if team_to_div[a] == team_to_div[b]:
                continue  # must be non-division
            key = frozenset((a, b))
            if key in game_keys:
                continue  # already have a game
            extra_pairs.append((a, b))

    random.shuffle(extra_pairs)

    for a, b in extra_pairs:
        if extra_needed[a] <= 0 or extra_needed[b] <= 0:
            continue

        shared_weeks = bye_weeks[a] & bye_weeks[b]
        if not shared_weeks:
            continue

        week_idx = random.choice(tuple(shared_weeks))

        home, away = (a, b) if random.choice((True, False)) else (b, a)
        schedule[week_idx].append((home, away))
        game_keys.add(frozenset((a, b)))

        extra_needed[a] -= 1
        extra_needed[b] -= 1

        bye_weeks[a].discard(week_idx)
        bye_weeks[b].discard(week_idx)

    return schedule


def compute_strength_of_schedule(teams: List[Dict], schedule: List[List[Tuple[str, str]]]) -> None:
    """
    Compute strength of schedule (SoS) for each team based on opponents'
    final win percentage. Mutates team dicts in-place and sets 'sos'.
    """
    name_to_team = {t["name"]: t for t in teams}

    # 1) Compute win percentage for each team
    win_pct: Dict[str, float] = {}
    for t in teams:
        games = t["wins"] + t["losses"] + t["ties"]
        if games == 0:
            win_pct[t["name"]] = 0.0
        else:
            win_pct[t["name"]] = (t["wins"] + 0.5 * t["ties"]) / games

    # 2) Build list of opponents from the schedule
    opponents: Dict[str, List[str]] = {t["name"]: [] for t in teams}

    for week in schedule:
        for home, away in week:
            if home not in opponents or away not in opponents:
                continue
            opponents[home].append(away)
            opponents[away].append(home)

    # 3) For each team, average opponent win_pct
    for name, opp_list in opponents.items():
        if not opp_list:
            sos = 0.0
        else:
            sos = sum(win_pct[opp] for opp in opp_list) / len(opp_list)
        name_to_team[name]["sos"] = sos


def team_ranking_key(team: Dict) -> Tuple[float, float, int, int]:
    """
    Ranking key used for division winners, wildcards, and seeding.

    Higher is better:
      1. Win percentage
      2. Strength of schedule (sos)
      3. Point differential
      4. Points for
    """
    games = team["wins"] + team["losses"] + team["ties"]
    win_pct = 0.0 if games == 0 else (team["wins"] + 0.5 * team["ties"]) / games
    sos = team.get("sos", 0.0)
    diff = team["points_for"] - team["points_against"]
    return (win_pct, sos, diff, team["points_for"])

def select_playoff_teams(teams: List[Dict], num_wildcards: int = 6) -> Dict[str, List[Dict]]:
    """
    Selects:
      - All division winners
      - num_wildcards best remaining teams

    Returns:
      {
        'qualified':          ordered list of playoff teams with 'seed' field assigned (1 = best),
        'failed_to_qualify':  list of teams that did not make the playoff field
      }
    """
    # Group by division
    divisions: Dict[str, List[Dict]] = {}
    for t in teams:
        divisions.setdefault(t["division"], []).append(t)

    # Pick division winners
    division_winners: List[Dict] = []
    for members in divisions.values():
        winner = max(members, key=team_ranking_key)
        division_winners.append(winner)

    for w in division_winners:
        w["is_division_winner"] = True

    # Use names for set membership (dicts are unhashable)
    winner_names = {w["name"] for w in division_winners}
    others = [t for t in teams if t["name"] not in winner_names]

    # Wildcards
    others_sorted = sorted(others, key=team_ranking_key, reverse=True)
    wildcards = others_sorted[:num_wildcards]

    # Seed ordering for playoff field
    div_sorted = sorted(division_winners, key=team_ranking_key, reverse=True)
    wc_sorted = sorted(wildcards, key=team_ranking_key, reverse=True)
    playoff_field = div_sorted + wc_sorted

    # Teams that didn't make it
    playoff_names = {t["name"] for t in playoff_field}
    failed_to_qualify = [t for t in teams if t["name"] not in playoff_names]

    # Assign seeds (1 = best)
    for i, t in enumerate(playoff_field, start=1):
        t["seed"] = i

    return {"qualified": playoff_field, "failed_to_qualify": failed_to_qualify}


def simulate_crossover_games(
    crossover_teams: List[Dict],
    team_ratings: Dict[str, Dict],
    regular_season_games: List[Dict[str, Any]],
    start_week: int,
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

            week_number = start_week + round_num - 1
            regular_season_games.append({
                "week": week_number,
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


def simulate_playoffs(
    playoff_teams: List[Dict],
    team_ratings: Dict[str, Dict],
    playoff_games: List[Dict[str, any]],
) -> Dict:
    """
    Single-elimination playoff, reseeded each round by seed.
    If a playoff game ties, winner is chosen by a coin-flip OT.

    Every round, all teams that have been eliminated so far
    play in consolation games, so everybody keeps playing
    until the champion is crowned.
    """
    print("\n=== PLAYOFFS ===\n")

    seeds = sorted(playoff_teams, key=lambda t: t["seed"])
    consolation_pool: List[Dict] = []

    round_num = 1

    while len(seeds) > 1:
        print(f"--- Playoff Round {round_num} ---")
        new_seeds: List[Dict] = []
        working = sorted(seeds, key=lambda t: t["seed"])
        round_losers: List[Dict] = []

        # If odd number of teams, top seed gets a bye
        if len(working) % 2 == 1:
            bye_team = working[0]
            print(f"{bye_team['name']} (Seed {bye_team['seed']}) gets a BYE")
            new_seeds.append(bye_team)
            working = working[1:]

        i, j = 0, len(working) - 1
        while i < j:
            home = working[i]
            away = working[j]

            print(f"Matchup: {home['name']} (Seed {home['seed']}) vs {away['name']} (Seed {away['seed']})")

            result = play_football_game(
                team_ratings[home["name"]],
                team_ratings[away["name"]],
            )
            home_points = result["Team 1"]
            away_points = result["Team 2"]

            print(f"  Final: {home['name']} {home_points} - {away['name']} {away_points}")

            playoff_games.append({
                "round": f"Round {round_num}",
                "home": home["name"],
                "away": away["name"],
                "home_score": home_points,
                "away_score": away_points,
                "is_championship": False,  # will mark final later
            })

            if home_points > away_points:
                winner, loser = home, away
            elif away_points > home_points:
                winner, loser = away, home
            else:
                winner = random.choice((home, away))
                loser = away if winner is home else home
                print(f"  Tie in regulation, {winner['name']} wins in OT (coin flip).")

            new_seeds.append(winner)
            round_losers.append(loser)
            i += 1
            j -= 1

        consolation_pool.extend(round_losers)

        print()

        # Consolation games
        if consolation_pool:
            print(f"--- Consolation Games Round {round_num} ---")
            cons_working = sorted(consolation_pool, key=lambda t: t["seed"])
            used = set()

            for idx, team_a in enumerate(cons_working):
                name_a = team_a["name"]
                if name_a in used:
                    continue

                opponent = None
                for team_b in cons_working[idx + 1:]:
                    name_b = team_b["name"]
                    if name_b in used or name_b == name_a:
                        continue
                    opponent = team_b
                    break

                if opponent is None:
                    continue

                home, away = team_a, opponent
                if random.choice((True, False)):
                    home, away = away, home

                result = play_football_game(
                    team_ratings[home["name"]],
                    team_ratings[away["name"]],
                )
                home_points = result["Team 1"]
                away_points = result["Team 2"]

                print(f"  {home['name']} {home_points} - {away_points} {away['name']}")

                used.add(home["name"])
                used.add(away["name"])

            print()

        seeds = sorted(new_seeds, key=lambda t: t["seed"])
        round_num += 1

    champion = seeds[0]
    print(f"=== CHAMPION: {champion['name']} (Seed {champion['seed']}) ===\n")

    if playoff_games:
        playoff_games[-1]["is_championship"] = True

    return champion


def _make_team(name: str, division: str) -> Dict:
    """Helper to build a fresh team dict with zeroed stats."""
    return {
        "name": name,
        "division": division,
        "wins": 0,
        "losses": 0,
        "ties": 0,
        "points_for": 0,
        "points_against": 0,
        "sos": 0.0,
    }


def run_league() -> None:
    # All 50 states, 10 divisions of 5 teams each
    teams: List[Dict] = [
        # New England
        _make_team("Maine", "New England"),
        _make_team("New Hampshire", "New England"),
        _make_team("Vermont", "New England"),
        _make_team("Massachusetts", "New England"),
        _make_team("Rhode Island", "New England"),

        # Mid-Atlantic
        _make_team("Connecticut", "Mid-Atlantic"),
        _make_team("New York", "Mid-Atlantic"),
        _make_team("New Jersey", "Mid-Atlantic"),
        _make_team("Pennsylvania", "Mid-Atlantic"),
        _make_team("Ohio", "Mid-Atlantic"),

        # Chesapeake
        _make_team("Maryland", "Chesapeake"),
        _make_team("Virginia", "Chesapeake"),
        _make_team("Delaware", "Chesapeake"),
        _make_team("North Carolina", "Chesapeake"),
        _make_team("South Carolina", "Chesapeake"),

        # Southeast
        _make_team("Georgia", "Southeast"),
        _make_team("Florida", "Southeast"),
        _make_team("Alabama", "Southeast"),
        _make_team("Mississippi", "Southeast"),
        _make_team("Louisiana", "Southeast"),

        # Southwest
        _make_team("Arizona", "Southwest"),
        _make_team("Texas", "Southwest"),
        _make_team("Nevada", "Southwest"),
        _make_team("Oklahoma", "Southwest"),
        _make_team("New Mexico", "Southwest"),

        # Great Lakes
        _make_team("Minnesota", "Great Lakes"),
        _make_team("Michigan", "Great Lakes"),
        _make_team("Indiana", "Great Lakes"),
        _make_team("Illinois", "Great Lakes"),
        _make_team("Wisconsin", "Great Lakes"),

        # Appalachia
        _make_team("Kentucky", "Appalachia"),
        _make_team("Tennessee", "Appalachia"),
        _make_team("Missouri", "Appalachia"),
        _make_team("West Virginia", "Appalachia"),
        _make_team("Arkansas", "Appalachia"),

        # Plains
        _make_team("North Dakota", "Plains"),
        _make_team("South Dakota", "Plains"),
        _make_team("Kansas", "Plains"),
        _make_team("Nebraska", "Plains"),
        _make_team("Iowa", "Plains"),

        # Rocky
        _make_team("Idaho", "Rocky"),
        _make_team("Utah", "Rocky"),
        _make_team("Montana", "Rocky"),
        _make_team("Wyoming", "Rocky"),
        _make_team("Colorado", "Rocky"),

        # Pacific
        _make_team("California", "Pacific"),
        _make_team("Oregon", "Pacific"),
        _make_team("Washington", "Pacific"),
        _make_team("Alaska", "Pacific"),
        _make_team("Hawaii", "Pacific"),
    ]

    # Load ratings for each team by name
    team_ratings = {t["name"]: load_team_ratings(t["name"]) for t in teams}

    # Generate schedule
    schedule = generate_regular_season_schedule(team_objs=teams)

    # Game logs
    regular_season_games: List[Dict[str, any]] = []
    playoff_games: List[Dict[str, any]] = []

    # Regular season
    for week_num, games in enumerate(schedule, start=1):
        print(f"Week {week_num}")
        for home_name, away_name in games:
            home_team_obj = get_team(teams, home_name)
            away_team_obj = get_team(teams, away_name)

            result = play_football_game(
                team_ratings[home_name],
                team_ratings[away_name],
            )

            home_points = result["Team 1"]
            away_points = result["Team 2"]

            print(f"  {home_name} {home_points} - {away_points} {away_name}")

            regular_season_games.append({
                "week": week_num,
                "home": home_name,
                "away": away_name,
                "home_score": home_points,
                "away_score": away_points,
                "division_game": (home_team_obj["division"] == away_team_obj["division"]),
            })

            home_team_obj["points_for"] += home_points
            home_team_obj["points_against"] += away_points
            away_team_obj["points_for"] += away_points
            away_team_obj["points_against"] += home_points

            if home_points > away_points:
                home_team_obj["wins"] += 1
                away_team_obj["losses"] += 1
            elif away_points > home_points:
                away_team_obj["wins"] += 1
                home_team_obj["losses"] += 1
            else:
                home_team_obj["ties"] += 1
                away_team_obj["ties"] += 1

        print()

    # Compute SoS
    compute_strength_of_schedule(teams, schedule)

    # Final regular season standings
    print("Final Regular Season Standings")

    def standings_key_for_print(t: Dict) -> Tuple[float, float, int, int]:
        wp, sos, diff, pf = team_ranking_key(t)
        # sort descending on each
        return (-wp, -sos, -diff, -pf)

    for t in sorted(teams, key=standings_key_for_print):
        games = t["wins"] + t["losses"] + t["ties"]
        wp = (t["wins"] + 0.5 * t["ties"]) / games if games > 0 else 0.0
        diff = t["points_for"] - t["points_against"]
        print(
            f"{t['name']} ({t['division']}): "
            f"{t['wins']}-{t['losses']}-{t['ties']}  "
            f"WP={wp:.3f}  SoS={t['sos']:.3f}  "
            f"PF={t['points_for']}  PA={t['points_against']}  DIFF={diff}"
        )

    # Playoff selection: all division winners + 6 wildcards
    playoff_result = select_playoff_teams(teams, num_wildcards=6)
    playoff_teams = playoff_result["qualified"]
    failed_to_qualify_teams = playoff_result["failed_to_qualify"]

    print("\nPlayoff Field (Seeds):")
    for t in sorted(playoff_teams, key=lambda x: x["seed"]):
        print(f"Seed {t['seed']}: {t['name']} ({t['division']})")

    # Conference Crossover Games
    last_regular_week = len(schedule)
    simulate_crossover_games(
        failed_to_qualify_teams,
        team_ratings,
        regular_season_games,
        start_week=last_regular_week + 1
    )

    # Playoffs
    champion = simulate_playoffs(playoff_teams, team_ratings, playoff_games)

    # Export everything to JSON
    export_league_to_json(
        teams=teams,
        regular_season_games=regular_season_games,
        playoff_games=playoff_games,
        output_path=OUTPUT_JSON,
        season_year=SEASON_YEAR,
        champion_team=champion["name"] if champion else None,
    )

    print(f"League data written to {OUTPUT_JSON}")


if __name__ == "__main__":
    run_league()

