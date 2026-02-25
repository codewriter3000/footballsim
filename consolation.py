from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Protocol, Sequence, Tuple
import random

from game import play_football_game


Team = Dict[str, Any]
Ratings = Dict[str, Dict[str, Any]]
Matchup = Tuple[Team, Team]


class ConsolationStrategy(Protocol):
    """
    Strategy for producing and simulating consolation games for a given round.
    """

    def make_matchups(self, round_num: int, consolation_pool: Sequence[Team]) -> List[Matchup]:
        """Return a list of matchups to play from the pool."""
        ...

    def pick_home_away(self, matchup: Matchup) -> Matchup:
        """Return (home, away) ordering for a matchup."""
        ...

    def record_round_tag(self, round_num: int) -> str:
        """Return the round label stored in game records."""
        ...

    def play_round(
        self,
        round_num: int,
        consolation_pool: List[Team],
        team_ratings: Ratings,
        consolation_games: List[Dict[str, Any]],
    ) -> None:
        """Simulate consolation games and append results to consolation_games."""
        ...


@dataclass(frozen=True)
class SeedNeighborFirstUnusedConsolation:
    """
    Default behavior matching your current function:
      - sort by seed
      - walk from lowest seed upward; pair each unused team with the first unused team after it
      - randomize home/away
      - teams can remain in the pool across rounds; this method only ensures
        a team plays at most once *per round*
    """

    def make_matchups(self, round_num: int, consolation_pool: Sequence[Team]) -> List[Matchup]:
        cons_working = sorted(consolation_pool, key=lambda t: t["seed"])
        used: set[str] = set()
        matchups: List[Matchup] = []

        for idx, team_a in enumerate(cons_working):
            name_a = team_a["name"]
            if name_a in used:
                continue

            opponent: Optional[Team] = None
            for team_b in cons_working[idx + 1 :]:
                name_b = team_b["name"]
                if name_b in used or name_b == name_a:
                    continue
                opponent = team_b
                break

            if opponent is None:
                continue

            matchups.append((team_a, opponent))
            used.add(team_a["name"])
            used.add(opponent["name"])

        return matchups

    def pick_home_away(self, matchup: Matchup) -> Matchup:
        a, b = matchup
        return (b, a) if random.choice((True, False)) else (a, b)

    def record_round_tag(self, round_num: int) -> str:
        return f"PC{round_num}"

    def play_round(
        self,
        round_num: int,
        consolation_pool: List[Team],
        team_ratings: Ratings,
        consolation_games: List[Dict[str, Any]],
    ) -> None:
        print(f"--- Consolation Games Round {round_num} ---")

        matchups = self.make_matchups(round_num, consolation_pool)

        for matchup in matchups:
            home, away = self.pick_home_away(matchup)

            result = play_football_game(
                team_ratings[home["name"]],
                team_ratings[away["name"]],
            )
            home_points = result["Team 1"]
            away_points = result["Team 2"]

            print(f"  {home['name']} {home_points} - {away_points} {away['name']}")

            consolation_games.append({
                "round": self.record_round_tag(round_num),
                "home": home["name"],
                "away": away["name"],
                "home_score": home_points,
                "away_score": away_points,
            })

        print()