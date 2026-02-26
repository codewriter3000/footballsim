from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Protocol, Sequence, Set, Tuple
import random

from ..game_logic.game import play_football_game


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
class NoRepeatConsolation:
    """
    Consolation pairing that avoids repeat matchups across ALL prior consolation rounds.

    Behavior:
      - sort by seed
      - pair each unused team with the first unused opponent it has NOT played before
      - if no unseen opponent exists, (optionally) allow a repeat as a fallback to avoid idling
      - randomize home/away
      - a team plays at most once per round
    """
    allow_repeat_if_stuck: bool = True

    def _played_pairs(self, consolation_games: Sequence[Dict[str, Any]]) -> Set[Tuple[str, str]]:
        """
        Normalize played matchups as unordered (min(name), max(name)) pairs.
        """
        played: Set[Tuple[str, str]] = set()
        for g in consolation_games:
            a, b = g["home"], g["away"]
            played.add((a, b) if a < b else (b, a))
        return played

    def make_matchups(
        self,
        round_num: int,
        consolation_pool: Sequence[Team],
        consolation_games: Sequence[Dict[str, Any]],
    ) -> List[Matchup]:
        cons_working = sorted(consolation_pool, key=lambda t: t["seed"])
        used: Set[str] = set()
        matchups: List[Matchup] = []
        played = self._played_pairs(consolation_games)

        def has_played(a: str, b: str) -> bool:
            key = (a, b) if a < b else (b, a)
            return key in played

        for idx, team_a in enumerate(cons_working):
            name_a = team_a["name"]
            if name_a in used:
                continue

            opponent: Optional[Team] = None

            # First pass: find an opponent team_a has NOT played before
            for team_b in cons_working[idx + 1 :]:
                name_b = team_b["name"]
                if name_b in used or name_b == name_a:
                    continue
                if not has_played(name_a, name_b):
                    opponent = team_b
                    break

            # Optional fallback: if stuck, allow the first available opponent (repeat)
            if opponent is None and self.allow_repeat_if_stuck:
                for team_b in cons_working[idx + 1 :]:
                    name_b = team_b["name"]
                    if name_b in used or name_b == name_a:
                        continue
                    opponent = team_b
                    break

            if opponent is None:
                continue

            matchups.append((team_a, opponent))
            used.add(name_a)
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

        matchups = self.make_matchups(
            round_num=round_num,
            consolation_pool=consolation_pool,
            consolation_games=consolation_games,
        )

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

            if home_points > away_points:
                home["wins"] += 1
                away["losses"] += 1
            elif away_points > home_points:
                away["wins"] += 1
                home["losses"] += 1
            else:
                home["ties"] += 1
                away["ties"] += 1

        print()