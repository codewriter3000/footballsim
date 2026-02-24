from fastapi import FastAPI, HTTPException
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
    
@app.get("/teams/{team_name}")
def get_team(team_name: str, season_year: int = 2025):
    formatted_team_name = team_name.replace("%20", " ")
    print(f"Getting team info for {formatted_team_name} in season {season_year}")
    file = DATA_DIR / f"league_{season_year}.json"
    if not file.exists():
        raise HTTPException(status_code=404, detail="Season not found")
    with file.open("r", encoding="utf-8") as f:
        data = json.load(f)
    team = next((t for t in data["teams"] if t["name"] == formatted_team_name), None)
    games = [g for g in data["regular_season_games"] if g["home"] == formatted_team_name or g["away"] == formatted_team_name]
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    print(team)
    print(games)
    return {"team": team, "games": games}

@app.get("/playoffs/{season_year}")
def get_playoffs(season_year: int = 2025):
    file = DATA_DIR / f"league_{season_year}.json"
    if not file.exists():
        raise HTTPException(status_code=404, detail="Season not found")
    with file.open("r", encoding="utf-8") as f:
        data = json.load(f)
    games = [g for g in data["playoff_games"]]
    print(games)
    return games