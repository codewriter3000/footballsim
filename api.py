from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pathlib import Path
import json

from league import simulate_league

app = FastAPI()
DATA_DIR = Path("seasons")

# Allows front-end server to connect to API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/simulate-season")
def simulate_season(
    season_year: Optional[int] = None,
    seed: Optional[int] = None,
):
    """
    Run a full season and return league data as JSON.
    """
    league_data = simulate_league(
        season_year=season_year or 2025,
        seed=seed,
        export_path=None,
        verbose=False,
    )
    return league_data

@app.get("/seasons/{year}")
def get_season(year: int = 2025):
    file = DATA_DIR / f"league_{year}.json"
    if not file.exists():
        raise HTTPException(status_code=404, detail="Season not found")
    with file.open("r", encoding="utf-8") as f:
        return json.load(f)

