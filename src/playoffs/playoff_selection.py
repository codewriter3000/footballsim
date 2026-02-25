from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Protocol, Sequence, Tuple


Team = Dict[str, Any]
SelectionResult = Dict[str, List[Team]]
RankKeyFn = Callable[[Team], Any]


class PlayoffSelectionStrategy(Protocol):
    """
    Strategy that decides who qualifies and how they are seeded.
    Must return:
      {
        "qualified": [teams... with 'seed' assigned],
        "failed_to_qualify": [...]
      }
    """

    def select(self, teams: Sequence[Team]) -> SelectionResult:
        ...


def _group_by_division(teams: Sequence[Team]) -> Dict[str, List[Team]]:
    divisions: Dict[str, List[Team]] = {}
    for t in teams:
        divisions.setdefault(t["division"], []).append(t)
    return divisions


@dataclass(frozen=True)
class DivisionWinnersPlusWildcards:
    """
    Default behavior matching your current function:
      - all division winners (by rank_key)
      - num_wildcards best remaining (by rank_key)
      - seeds assigned 1..N using rank_key ordering (division winners first, then wildcards),
        but both sublists are individually sorted by rank_key desc (your current behavior).
    """
    rank_key: RankKeyFn
    num_wildcards: int = 6
    mark_division_winners: bool = True

    def select(self, teams: Sequence[Team]) -> SelectionResult:
        # Group by division
        divisions = _group_by_division(teams)

        # Pick division winners
        division_winners: List[Team] = []
        for members in divisions.values():
            winner = max(members, key=self.rank_key)
            division_winners.append(winner)

        # Sort division winners by ranking
        division_winners.sort(key=self.rank_key, reverse=True)

        if self.mark_division_winners:
            for w in division_winners:
                w["is_division_winner"] = True

        winner_names = {w["name"] for w in division_winners}
        others = [t for t in teams if t["name"] not in winner_names]

        # Wildcards
        others_sorted = sorted(others, key=self.rank_key, reverse=True)
        wildcards = others_sorted[: self.num_wildcards]

        # Seed ordering for playoff field (matches your code)
        div_sorted = sorted(division_winners, key=self.rank_key, reverse=True)
        wc_sorted = sorted(wildcards, key=self.rank_key, reverse=True)
        playoff_field = div_sorted + wc_sorted

        # Failed to qualify
        playoff_names = {t["name"] for t in playoff_field}
        failed_to_qualify = [t for t in teams if t["name"] not in playoff_names]

        # Assign seeds (1 = best)
        for i, t in enumerate(playoff_field, start=1):
            t["seed"] = i

        return {"qualified": playoff_field, "failed_to_qualify": failed_to_qualify}
