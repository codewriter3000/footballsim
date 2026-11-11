SEASON_YEAR: int | None = None
COMPETITION_CONSTANT: float | None = None

_initialized = False


def init(season_year: int, competition_constant: float) -> None:
    """
    Initialize global constants once at application startup.
    """
    global SEASON_YEAR, COMPETITION_CONSTANT, _initialized

    if _initialized:
        raise RuntimeError("constants already initialized")

    SEASON_YEAR = season_year
    COMPETITION_CONSTANT = competition_constant
    _initialized = True


def ensure_initialized() -> None:
    if not _initialized:
        raise RuntimeError("constants not initialized. Call constants.init() first.")
