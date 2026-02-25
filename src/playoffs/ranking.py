from typing import Any, Callable, Dict, Tuple

Team = Dict[str, Any]
RankKey = Callable[[Team], Tuple[Any, ...]]  # tuple so Python can lexicographically compare

def rank_default(team: Team) -> Tuple[float, float, int, int]:
    games = team["wins"] + team["losses"] + team["ties"]
    win_pct = 0.0 if games == 0 else (team["wins"] + 0.5 * team["ties"]) / games
    sos = team.get("sos", 0.0)
    diff = team["points_for"] - team["points_against"]
    return (win_pct, sos, diff, team["points_for"])
