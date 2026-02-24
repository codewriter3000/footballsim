import random
from typing import Dict, List

from game import play_football_game


def simulate_consolation_games(round_num: int, 
                               consolation_pool: List[Dict], 
                               team_ratings: Dict[str, Dict], 
                               consolation_games: List[Dict[str, any]]):
    
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

        consolation_games.append({
            "round": f"PC{round_num}",
            "home": home["name"],
            "away": away["name"],
            "home_score": home_points,
            "away_score": away_points,
        })

        used.add(home["name"])
        used.add(away["name"])

    print()


def simulate_playoffs(
    playoff_teams: List[Dict],
    team_ratings: Dict[str, Dict],
    playoff_games: List[Dict[str, any]],
    consolation_games: List[Dict[str, any]],
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
            simulate_consolation_games(
                round_num=round_num,
                consolation_pool=consolation_pool,
                team_ratings=team_ratings,
                consolation_games=consolation_games,
            )

        seeds = sorted(new_seeds, key=lambda t: t["seed"])
        round_num += 1

    champion = seeds[0]
    print(f"=== CHAMPION: {champion['name']} (Seed {champion['seed']}) ===\n")

    if playoff_games:
        playoff_games[-1]["is_championship"] = True

    return champion