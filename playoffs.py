from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Protocol, Sequence, Tuple
import random

from consolation import ConsolationStrategy, SeedNeighborFirstUnusedConsolation
from game import play_football_game

Team = Dict[str, Any]
Ratings = Dict[str, Dict[str, Any]]
Matchup = Tuple[Team, Team]


class SeedingStrategy(Protocol):
    """
    A strategy that decides:
      - which team (if any) gets a bye
      - how to pair teams into matchups for this round
      - how to order / re-seed teams after the round (optional)
    """

    def order_for_round(self, teams: Sequence[Team]) -> List[Team]:
        """Return teams in the order used to decide byes + matchups."""
        ...

    def pick_bye(self, ordered: Sequence[Team]) -> Tuple[Optional[Team], List[Team]]:
        """Return (bye_team_or_none, remaining_teams_to_pair)."""
        ...

    def make_matchups(self, to_pair: Sequence[Team]) -> List[Matchup]:
        """Return list of (home, away) pairs for this round."""
        ...

    def reseed_after_round(self, advancing: Sequence[Team]) -> List[Team]:
        """Return teams for the next round (can reseed or preserve bracket)."""
        ...


@dataclass(frozen=True)
class HighVsLowReseedEachRound:
    """
    Your current behavior:
      - sort by seed each round
      - if odd, top seed gets bye
      - pair highest vs lowest
      - reseed (sort) again for next round
    """

    def order_for_round(self, teams: Sequence[Team]) -> List[Team]:
        return sorted(teams, key=lambda t: t["seed"])

    def pick_bye(self, ordered: Sequence[Team]) -> Tuple[Optional[Team], List[Team]]:
        working = list(ordered)
        if len(working) % 2 == 1:
            return working[0], working[1:]
        return None, working

    def make_matchups(self, to_pair: Sequence[Team]) -> List[Matchup]:
        working = list(to_pair)
        matchups: List[Matchup] = []
        i, j = 0, len(working) - 1
        while i < j:
            matchups.append((working[i], working[j]))
            i += 1
            j -= 1
        return matchups

    def reseed_after_round(self, advancing: Sequence[Team]) -> List[Team]:
        return sorted(list(advancing), key=lambda t: t["seed"])


def resolve_winner_by_score_or_coinflip(home: Team, away: Team, home_points: int, away_points: int) -> Tuple[Team, Team, bool]:
    """Returns (winner, loser, decided_by_coinflip_ot)."""
    if home_points > away_points:
        return home, away, False
    if away_points > home_points:
        return away, home, False
    winner = random.choice((home, away))
    loser = away if winner is home else home
    return winner, loser, True


def simulate_playoffs(
    playoff_teams: List[Team],
    team_ratings: Ratings,
    playoff_games: List[Dict[str, Any]],
    consolation_games: List[Dict[str, Any]],
    seeding: SeedingStrategy = HighVsLowReseedEachRound(),
    consolation: ConsolationStrategy = SeedNeighborFirstUnusedConsolation(),
) -> Team:
    """
    Single-elimination playoffs with swap-in seeding strategy.
    Every round, eliminated teams join the consolation pool and keep playing.
    """
    print("\n=== PLAYOFFS ===\n")

    seeds: List[Team] = list(playoff_teams)
    consolation_pool: List[Team] = []
    round_num = 1

    while len(seeds) > 1:
        print(f"--- Playoff Round {round_num} ---")

        ordered = seeding.order_for_round(seeds)
        bye_team, to_pair = seeding.pick_bye(ordered)

        advancing: List[Team] = []
        round_losers: List[Team] = []

        if bye_team is not None:
            print(f"{bye_team['name']} (Seed {bye_team['seed']}) gets a BYE")
            advancing.append(bye_team)

        matchups = seeding.make_matchups(to_pair)

        for home, away in matchups:
            print(f"Matchup: {home['name']} (Seed {home['seed']}) vs {away['name']} (Seed {away['seed']})")

            result = play_football_game(
                team_ratings[home["name"]],
                team_ratings[away["name"]],
                playoffs=True,
            )
            home_points = result["Team 1"]
            away_points = result["Team 2"]

            print(f"  Final: {home['name']} {home_points} - {away['name']} {away_points}")

            winner, loser, coinflip = resolve_winner_by_score_or_coinflip(home, away, home_points, away_points)
            if coinflip:
                print(f"  Tie in regulation, {winner['name']} wins in OT (coin flip).")

            playoff_games.append({
                "round": f"Round {round_num}",
                "home": home["name"],
                "away": away["name"],
                "home_score": home_points,
                "away_score": away_points,
                "is_championship": False,  # mark final later
            })

            advancing.append(winner)
            round_losers.append(loser)

        consolation_pool.extend(round_losers)
        print()

        if consolation_pool:
            consolation.play_round(
                round_num=round_num,
                consolation_pool=consolation_pool,
                team_ratings=team_ratings,
                consolation_games=consolation_games,
            )
            # simulate_consolation_games(
            #     round_num=round_num,
            #     consolation_pool=consolation_pool,
            #     team_ratings=team_ratings,
            #     consolation_games=consolation_games,
            # )

        seeds = seeding.reseed_after_round(advancing)
        round_num += 1

    champion = seeds[0]
    print(f"=== CHAMPION: {champion['name']} (Seed {champion['seed']}) ===\n")

    if playoff_games:
        playoff_games[-1]["is_championship"] = True

    return champion
