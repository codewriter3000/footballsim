from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Protocol, Sequence, Tuple
import random

from .consolation import ConsolationStrategy, NoRepeatConsolation
from ..game_logic.game import play_football_game

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


@dataclass(frozen=True)
class FairBracket16NoReseed:
    """
    True fixed 16-team bracket (no reseeding) that advances like a real bracket:

    Round of 16:
      (1 v 16) plays winner into Quarterfinal A
      (8 v 9)  plays winner into Quarterfinal A

      (4 v 13) plays winner into Quarterfinal B
      (5 v 12) plays winner into Quarterfinal B

      (2 v 15) plays winner into Quarterfinal C
      (7 v 10) plays winner into Quarterfinal C

      (3 v 14) plays winner into Quarterfinal D
      (6 v 11) plays winner into Quarterfinal D

    Then:
      - QF: A vs A, B vs B, C vs C, D vs D
      - SF: winner(QF1) vs winner(QF2), winner(QF3) vs winner(QF4)
      - F: winner(SF1) vs winner(SF2)

    Requirements:
      - Exactly 16 teams to start.
      - Your simulate_playoffs loop MUST preserve the returned order from
        reseed_after_round() (i.e., must not re-sort by seed for this strategy).
    """

    # Bracket "slots" in the exact order they should be paired each round.
    # If we keep winners in this order, then pairing adjacent teams each round
    # yields correct bracket progression.
    _round_of_16_slots: Tuple[Tuple[int, int], ...] = (
        (1, 16),
        (8, 9),
        (4, 13),
        (5, 12),
        (2, 15),
        (7, 10),
        (3, 14),
        (6, 11),
    )

    def order_for_round(self, teams: Sequence[Team]) -> List[Team]:
        # For a fixed bracket we do NOT want reseeding each round.
        # We'll treat the incoming `teams` order as the bracket order.
        return list(teams)

    def pick_bye(self, ordered: Sequence[Team]) -> Tuple[Optional[Team], List[Team]]:
        # No byes ever (in a 16-team fixed bracket).
        return None, list(ordered)

    def make_matchups(self, to_pair: Sequence[Team]) -> List[Matchup]:
        n = len(to_pair)

        # Round 1: build bracket order from seeds and return the 8 correct matchups.
        if n == 16:
            by_seed = {t["seed"]: t for t in to_pair}
            missing = [s for s in range(1, 17) if s not in by_seed]
            if missing:
                raise ValueError(f"Missing required seeds for 16-team bracket: {missing}")

            # IMPORTANT: return matchups in bracket order:
            # matchups[0] winner faces matchups[1] winner next round, etc.
            return [(by_seed[a], by_seed[b]) for a, b in self._round_of_16_slots]

        # Later rounds: pair adjacent teams in the current bracket order.
        if n % 2 != 0:
            raise ValueError(f"Fixed bracket requires an even number of teams each round; got {n}")

        matchups: List[Matchup] = []
        for i in range(0, n, 2):
            matchups.append((to_pair[i], to_pair[i + 1]))
        return matchups

    def reseed_after_round(self, advancing: Sequence[Team]) -> List[Team]:
        # Preserve bracket order exactly as winners were produced.
        # Because make_matchups() returns matchups in bracket order,
        # appending winners in that same order ensures proper progression.
        return list(advancing)


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
    seeding: SeedingStrategy = FairBracket16NoReseed(),
    consolation: ConsolationStrategy = NoRepeatConsolation(),
) -> Team:
    """
    Single-elimination playoffs with swap-in seeding strategy.

    Constraint:
      If there are N playoff rounds (including the championship round),
      then there are exactly N-1 consolation rounds.

    Implementation:
      - We simulate consolation at the *start* of each playoff round AFTER Round 1
        (i.e., rounds 2..N). That yields exactly N-1 consolation rounds.
      - Losers from the current playoff round are added to the consolation pool,
        but they don't play until the *next* consolation round.
    """
    print("\n=== PLAYOFFS ===\n")

    seeds: List[Team] = list(playoff_teams)
    consolation_pool: List[Team] = []
    round_num = 1

    while len(seeds) > 1:
        print(f"--- Playoff Round {round_num} ---")

        # Consolation happens for rounds 2..N (i.e., N-1 times total).
        # Important: This uses the pool accumulated from *previous* playoff round losers.
        if round_num > 1 and consolation_pool:
            consolation.play_round(
                round_num=round_num - 1,  # label consolation rounds as 1..N-1
                consolation_pool=consolation_pool,
                team_ratings=team_ratings,
                consolation_games=consolation_games,
            )

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

            if home_points > away_points:
                home["wins"] += 1
                away["losses"] += 1
            elif away_points > home_points:
                away["wins"] += 1
                home["losses"] += 1
            else:
                home["ties"] += 1
                away["ties"] += 1

            advancing.append(winner)
            round_losers.append(loser)

        # Add losers AFTER consolation for this loop iteration,
        # so they play in the next consolation round (if any).
        consolation_pool.extend(round_losers)

        print()
        seeds = seeding.reseed_after_round(advancing)
        round_num += 1

    champion = seeds[0]
    print(f"=== CHAMPION: {champion['name']} (Seed {champion['seed']}) ===\n")

    if playoff_games:
        playoff_games[-1]["is_championship"] = True

    return champion