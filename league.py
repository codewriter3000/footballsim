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
      - 2 non-division games per team via pairing
      - 1 additional non-division game scheduled on a shared bye week
        (when structure allows)

    Returns: list of weeks, where each week is a list of (home, away) tuples.
    """
    # Map names to divisions and group by division
    divisions = {}
    team_to_div = {}

    for t in team_objs:
        name = t["name"]
        div = t.get("division", "DIV1")
        team_to_div[name] = div
        divisions.setdefault(div, []).append(name)

    team_names = [t["name"] for t in team_objs]

    # --- 1. Divisional games ---
    all_games = []
    game_keys = set()  # frozenset({team1, team2}) to avoid duplicates

    for div, names in divisions.items():
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

    # --- 2. Non-division games: aim for 2 per team via normal pairing ---
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
                continue  # already scheduled (safety)

            # Randomize home/away
            if random.choice((True, False)):
                game = (a, b)
            else:
                game = (b, a)

            all_games.append(game)
            game_keys.add(key)
            cross_needed[a] -= 1
            cross_needed[b] -= 1
        # Some teams may get fewer than 2 if structure prevents perfect pairing.

    # --- 3. Pack games into weeks (each team at most once per week) ---
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

    # --- 4. Compute bye weeks for each team ---
    num_weeks = len(schedule)
    bye_weeks = {name: set(range(num_weeks)) for name in team_names}

    for week_idx, games in enumerate(schedule):
        for home, away in games:
            bye_weeks[home].discard(week_idx)
            bye_weeks[away].discard(week_idx)

    # --- 5. Use shared bye weeks to add a 3rd non-division game ---
    # Each team *aims* to get 1 extra non-division game on a shared bye week
    extra_needed = {name: 1 for name in team_names}

    # Build candidate cross-division pairs that have not yet played
    extra_pairs = []
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

        # Find a week where BOTH have a bye
        shared_weeks = bye_weeks[a] & bye_weeks[b]
        if not shared_weeks:
            continue

        # Pick a shared bye week and schedule the extra game there
        week_idx = random.choice(tuple(shared_weeks))

        # Randomize home/away
        if random.choice((True, False)):
            game = (a, b)
        else:
            game = (b, a)

        schedule[week_idx].append(game)
        game_keys.add(frozenset((a, b)))

        extra_needed[a] -= 1
        extra_needed[b] -= 1

        # They no longer have a bye that week
        bye_weeks[a].discard(week_idx)
        bye_weeks[b].discard(week_idx)

    # Some teams might still have extra_needed > 0 if structure/bye alignment
    # makes it impossible. They will stay with 2 non-division games.

    return schedule



def compute_strength_of_schedule(teams, schedule):
    """
    Compute strength of schedule (SoS) for each team based on opponents'
    final win percentage.
    """
    name_to_team = {t["name"]: t for t in teams}

    # 1) Compute win percentage for each team
    win_pct = {}
    for t in teams:
        games = t["wins"] + t["losses"] + t["ties"]
        if games == 0:
            win_pct[t["name"]] = 0.0
        else:
            win_pct[t["name"]] = (t["wins"] + 0.5 * t["ties"]) / games

    # 2) Build list of opponents from the schedule
    opponents = {t["name"]: [] for t in teams}

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


def team_ranking_key(team):
    """
    Ranking key used for division winners, wildcards, and seeding.

    Higher is better:
      1. Win percentage
      2. Strength of schedule (sos)
      3. Point differential
      4. Points for
    """
    games = team["wins"] + team["losses"] + team["ties"]
    if games == 0:
        win_pct = 0.0
    else:
        win_pct = (team["wins"] + 0.5 * team["ties"]) / games

    sos = team.get("sos", 0.0)
    diff = team["points_for"] - team["points_against"]
    return (win_pct, sos, diff, team["points_for"])


def select_playoff_teams(teams, num_wildcards=6):
    """
    Selects:
      - All division winners
      - num_wildcards best remaining teams

    Returns ordered list of playoff teams with 'seed' field assigned (1 = best).
    """
    # Group by division
    divisions = {}
    for t in teams:
        divisions.setdefault(t["division"], []).append(t)

    division_winners = []
    for _, members in divisions.items():
        winner = max(members, key=team_ranking_key)
        division_winners.append(winner)

    for w in division_winners:
        w["is_division_winner"] = True

    winners_set = {t["name"] for t in division_winners}
    others = [t for t in teams if t["name"] not in winners_set]

    others_sorted = sorted(others, key=team_ranking_key, reverse=True)
    wildcards = others_sorted[:num_wildcards]

    div_sorted = sorted(division_winners, key=team_ranking_key, reverse=True)
    wc_sorted = sorted(wildcards, key=team_ranking_key, reverse=True)
    failed_to_qualify = [t for t in others if t["name"] not in winners_set or wildcards]

    playoff_field = div_sorted + wc_sorted

    for i, t in enumerate(playoff_field, start=1):
        t["seed"] = i

    return {'qualified': playoff_field, 'failed_to_qualify': failed_to_qualify}


def simulate_crossover_games(crossover_teams, team_ratings, target_games=10):
    """
    Schedule and simulate 'conference crossover' games for teams that did not
    make the playoffs.

    Every non-playoff team is *guaranteed* up to `target_games` total games
    (regular season + crossover). We infer current games from wins/losses/ties.

    We fake two conferences by grouping divisions:
      - East Conf:  New England, Mid-Atlantic, Chesapeake, Southeast, Gulf
      - West Conf:  Great Lakes, Heartland, Plains, Mountain, Pacific

    Only games between East/West are scheduled here.
    """
    if not crossover_teams:
        return

    print("\n=== CROSSOVERS ===\n")

    # Map divisions to pseudo-conferences
    east_divs = {
        "New England",
        "Mid-Atlantic",
        "Chesapeake",
        "Southeast",
        "Gulf",
    }
    west_divs = {
        "Great Lakes",
        "Heartland",
        "Plains",
        "Mountain",
        "Pacific",
    }

    # Build per-team state (do not mutate team list structure itself)
    team_state = {}
    already_played = set()  # track crossover matchups we create here

    for t in crossover_teams:
        name = t["name"]
        games_played = t["wins"] + t["losses"] + t["ties"]
        division = t.get("division", "")
        if division in east_divs:
            conference = "East"
        elif division in west_divs:
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
        # Teams still needing games
        needing = [ts for ts in team_state.values() if ts["needed"] > 0]

        # Stop if fewer than 2 teams still need games
        if len(needing) < 2:
            break

        # Sort so the teams with the fewest games get paired first
        needing.sort(key=lambda ts: (ts["games_played"], ts["name"]))

        print(f"--- Crossover Week {round_num} ---")
        used_this_round = set()
        made_pair = False

        for ts in needing:
            name = ts["name"]
            if ts["needed"] <= 0 or name in used_this_round:
                continue

            # Only schedule cross-conference games (East vs West)
            conf = ts["conference"]
            if conf not in ("East", "West"):
                continue

            desired_opponent_conf = "West" if conf == "East" else "East"

            # First try to find an opponent in opposite conference,
            # who also still needs games, who is free this week,
            # and who has not already been a crossover opponent.
            opponent_ts = None
            for cand in needing:
                cname = cand["name"]
                if cname == name:
                    continue
                if cand["needed"] <= 0:
                    continue
                if cname in used_this_round:
                    continue
                if cand["conference"] != desired_opponent_conf:
                    continue

                matchup_key = frozenset((name, cname))
                if matchup_key in already_played:
                    continue

                opponent_ts = cand
                break

            # If we cannot find a 'fresh' opponent, allow a repeat
            if opponent_ts is None:
                for cand in needing:
                    cname = cand["name"]
                    if cname == name:
                        continue
                    if cand["needed"] <= 0:
                        continue
                    if cname in used_this_round:
                        continue
                    if cand["conference"] != desired_opponent_conf:
                        continue
                    opponent_ts = cand
                    break

            if opponent_ts is None:
                # No valid cross-conference opponent for this team this week
                continue

            home_name, away_name = name, opponent_ts["name"]
            # Randomize home/away
            if random.choice((True, False)):
                home_name, away_name = away_name, home_name

            # Simulate the game (Team 1 = home, Team 2 = away)
            result = play_football_game(
                team_ratings[home_name],
                team_ratings[away_name],
            )
            home_points = result["Team 1"]
            away_points = result["Team 2"]

            print(f"  {home_name} {home_points} - {away_points} {away_name}")

            # Update original team dicts' stats
            home_team = team_state[home_name]["team"]
            away_team = team_state[away_name]["team"]

            home_team["points_for"]     += home_points
            home_team["points_against"] += away_points
            away_team["points_for"]     += away_points
            away_team["points_against"] += home_points

            if home_points > away_points:
                home_team["wins"]  += 1
                away_team["losses"] += 1
            elif away_points > home_points:
                away_team["wins"]  += 1
                home_team["losses"] += 1
            else:
                home_team["ties"]  += 1
                away_team["ties"]  += 1

            # Update per-team state
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


def simulate_playoffs(playoff_teams, team_ratings):
    """
    Single-elimination playoff, reseeded each round by seed.
    If a playoff game ties, winner is chosen by a coin-flip OT.

    NEW: Every round, all teams that have been eliminated so far
    play in consolation games, so everybody keeps playing
    until the champion is crowned.
    """
    print("\n=== PLAYOFFS ===\n")

    # Seeds still alive for the championship
    seeds = sorted(playoff_teams, key=lambda t: t["seed"])
    # All teams eliminated from title contention so far
    consolation_pool = []

    round_num = 1

    while len(seeds) > 1:
        print(f"--- Playoff Round {round_num} ---")
        new_seeds = []
        working = sorted(seeds, key=lambda t: t["seed"])

        round_losers = []

        # If odd number of teams, top seed gets a bye
        if len(working) % 2 == 1:
            bye_team = working[0]
            print(f"{bye_team['name']} (Seed {bye_team['seed']}) gets a BYE")
            new_seeds.append(bye_team)
            working = working[1:]

        # Highest vs lowest, like before
        i = 0
        j = len(working) - 1
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

            print(f"  Final: {home['name']} {home_points} - {away_points} {away['name']}")

            if home_points > away_points:
                winner = home
                loser = away
            elif away_points > home_points:
                winner = away
                loser = home
            else:
                winner = random.choice((home, away))
                loser = home if winner is away else away
                print(f"  Tie in regulation, {winner['name']} wins in OT (coin flip).")

            new_seeds.append(winner)
            round_losers.append(loser)

            i += 1
            j -= 1

        # Add this round's losers to the consolation pool
        consolation_pool.extend(round_losers)

        print()

        # --- Consolation games for everyone eliminated so far ---
        if consolation_pool:
            print(f"--- Consolation Games Round {round_num} ---")
            # Sort by seed for a stable, nice-looking schedule
            cons_working = sorted(consolation_pool, key=lambda t: t["seed"])
            used = set()

            for idx, team_a in enumerate(cons_working):
                name_a = team_a["name"]
                if name_a in used:
                    continue

                # Find the next available opponent in consolation_pool
                opponent = None
                for team_b in cons_working[idx + 1:]:
                    name_b = team_b["name"]
                    if name_b in used or name_b == name_a:
                        continue
                    opponent = team_b
                    break

                if opponent is None:
                    # Odd team out this round; no consolation game
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

        # Advance winners in the title bracket
        seeds = sorted(new_seeds, key=lambda t: t["seed"])
        round_num += 1

    # Final champion
    champion = seeds[0]
    print(f"=== CHAMPION: {champion['name']} (Seed {champion['seed']}) ===\n")
    return champion


def run_league():
    # All 50 states, 10 divisions of 5 teams each
    teams = [
        # New England
        {"name": "Maine",          "division": "New England", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "New Hampshire",  "division": "New England", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "Vermont",        "division": "New England", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "Massachusetts",  "division": "New England", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "Rhode Island",   "division": "New England", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},

        # Mid-Atlantic
        {"name": "Connecticut",    "division": "Mid-Atlantic", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "New York",       "division": "Mid-Atlantic", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "New Jersey",     "division": "Mid-Atlantic", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "Pennsylvania",   "division": "Mid-Atlantic", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "Delaware",       "division": "Mid-Atlantic", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},

        # Chesapeake
        {"name": "Maryland",       "division": "Chesapeake", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "Virginia",       "division": "Chesapeake", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "West Virginia",  "division": "Chesapeake", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "North Carolina", "division": "Chesapeake", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "South Carolina", "division": "Chesapeake", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},

        # Southeast
        {"name": "Georgia",        "division": "Southeast", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "Florida",        "division": "Southeast", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "Alabama",        "division": "Southeast", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "Mississippi",    "division": "Southeast", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "Tennessee",      "division": "Southeast", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},

        # Gulf
        {"name": "Louisiana",      "division": "Gulf", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "Texas",          "division": "Gulf", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "Arkansas",       "division": "Gulf", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "Oklahoma",       "division": "Gulf", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "New Mexico",     "division": "Gulf", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},

        # Great Lakes
        {"name": "Ohio",           "division": "Great Lakes", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "Michigan",       "division": "Great Lakes", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "Indiana",        "division": "Great Lakes", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "Illinois",       "division": "Great Lakes", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "Wisconsin",      "division": "Great Lakes", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},

        # Heartland
        {"name": "Minnesota",      "division": "Heartland", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "Iowa",           "division": "Heartland", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "Missouri",       "division": "Heartland", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "Kansas",         "division": "Heartland", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "Nebraska",       "division": "Heartland", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},

        # Plains
        {"name": "North Dakota",   "division": "Plains", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "South Dakota",   "division": "Plains", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "Montana",        "division": "Plains", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "Wyoming",        "division": "Plains", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "Colorado",       "division": "Plains", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},

        # Mountain
        {"name": "Idaho",          "division": "Mountain", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "Utah",           "division": "Mountain", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "Arizona",        "division": "Mountain", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "Nevada",         "division": "Mountain", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "Kentucky",       "division": "Mountain", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},

        # Pacific
        {"name": "California",     "division": "Pacific", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "Oregon",         "division": "Pacific", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "Washington",     "division": "Pacific", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "Alaska",         "division": "Pacific", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
        {"name": "Hawaii",         "division": "Pacific", "wins": 0, "losses": 0, "ties": 0,
         "points_for": 0, "points_against": 0, "sos": 0.0},
    ]

    # Load ratings for each team by name
    team_ratings = {t["name"]: load_team_ratings(t["name"]) for t in teams}

    # Generate schedule
    schedule = generate_regular_season_schedule(team_objs=teams)

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

            home_team_obj["points_for"]     += home_points
            home_team_obj["points_against"] += away_points
            away_team_obj["points_for"]     += away_points
            away_team_obj["points_against"] += home_points

            if home_points > away_points:
                home_team_obj["wins"]  += 1
                away_team_obj["losses"] += 1
            elif away_points > home_points:
                away_team_obj["wins"]  += 1
                home_team_obj["losses"] += 1
            else:
                home_team_obj["ties"]  += 1
                away_team_obj["ties"]  += 1

        print()

    # Compute SoS
    compute_strength_of_schedule(teams, schedule)

    # Final regular season standings
    print("Final Regular Season Standings")

    def standings_key_for_print(t):
        wp, sos, diff, pf = team_ranking_key(t)
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
    playoff_teams = select_playoff_teams(teams, num_wildcards=6)['qualified']
    failed_to_qualify_teams = select_playoff_teams(teams, num_wildcards=6)['failed_to_qualify']

    print("\nPlayoff Field (Seeds):")
    for t in sorted(playoff_teams, key=lambda x: x["seed"]):
        print(f"Seed {t['seed']}: {t['name']} ({t['division']})")

    # Conference Crossover Games
    simulate_crossover_games(failed_to_qualify_teams, team_ratings)

    # Playoffs
    simulate_playoffs(playoff_teams, team_ratings)


if __name__ == "__main__":
    run_league()

