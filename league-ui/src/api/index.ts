export const API_BASE_URL =
    import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000';

/* ---------- Types shared with your backend ---------- */

export interface Team {
  name: string;
  division: string;
  conference?: string | null;

  // season stats directly on team (from league.py)
  wins: number;
  losses: number;
  ties: number;
  points_for: number;
  points_against: number;
  sos?: number;
  is_division_winner?: boolean;
  seed?: number;
}

export interface RegularSeasonGame {
  week: number;
  home: string;
  away: string;
  home_score: number;
  away_score: number;
  division_game?: boolean;
}

export interface PlayoffGame {
  round: string; // e.g. "Round 1", "Round 2", "Championship"
  home: string;
  away: string;
  home_score: number;
  away_score: number;
  is_championship?: boolean;
}

/**
 * Optional: matches the shape produced inside records.py (teams_stats)
 * If you don't need this in the UI yet, you can treat it as Record<string, any>.
 */
export interface TeamSeasonStatsBlock {
  games_played: number;
  wins: number;
  losses: number;
  ties: number;
  points_for: number;
  points_against: number;
}

export interface TeamTitlesBlock {
  division_champion: boolean;
  championships: number;
}

export interface TeamStats {
  division: string;
  losses: number;
  name: string;
  points_against: number;
  points_for: number;
  sos: number;
  ties: number;
  wins: number;
  regular_season: TeamSeasonStatsBlock;
  playoffs: {
    berth: boolean;
    games_played: number;
    wins: number;
    losses: number;
    ties: number;
    points_for: number;
    points_against: number;
  };
  titles: TeamTitlesBlock;
}

export interface LeagueData {
  season_year: number | null;
  teams: Team[];
  teams_stats?: Record<string, TeamStats>;
  regular_season_games: RegularSeasonGame[];
  playoff_games: PlayoffGame[];
  champion?: string | null;
}

export type Game = {
  away: string;
  away_score: number;
  home: string;
  home_score: number;
  week: number;
  division_game: boolean;
};

export type TeamInfoResponse = {
  team: TeamStats;
  games: Game[];
};

/* ---------- Helpers ---------- */

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    const msg = text || `HTTP ${res.status}`;
    throw new Error(msg);
  }
  return res.json() as Promise<T>;
}

/* ---------- API functions ---------- */

/**
 * Run a new season on the backend and return the full league data.
 * This calls POST /simulate-season with a JSON body.
 */
export async function simulateSeason(params: {
  seasonYear?: number;
  seed?: number | null;
}): Promise<LeagueData> {
  const body: any = {};
  if (params.seasonYear !== undefined) body.season_year = params.seasonYear;
  if (params.seed !== undefined) body.seed = params.seed;

  const res = await fetch(`${API_BASE_URL}/simulate-season`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  return handleResponse<LeagueData>(res);
}

/**
 * Get the JSON for a particular season that has already been generated
 * and stored on disk (served by the backend).
 *
 * Assumes a GET /seasons/{year} endpoint.
 */
export async function getSeason(year: number): Promise<LeagueData> {
  const res = await fetch(`${API_BASE_URL}/seasons/${year}`, {
    method: "GET",
  });
  return handleResponse<LeagueData>(res);
}

/**
 * List available seasons (e.g. [2023, 2024, 2025]).
 *
 * Assumes a GET /seasons endpoint returning an array of years.
 */
export async function listSeasons(): Promise<number[]> {
  const res = await fetch(`${API_BASE_URL}/seasons`, {
    method: "GET",
  });
  return handleResponse<number[]>(res);
}

/**
 * Get information about a specific team for a given season.
 * Assumes a GET /seasons/{year}/teams/{teamName} endpoint.
 */
export async function getTeamInfo(
  year: number,
  teamName: string | null
): Promise<TeamInfoResponse> {
  if (!teamName) throw new Error("Team name is required");

  const res = await fetch(
    `${API_BASE_URL}/teams/${encodeURIComponent(teamName)}?year=${year}`,
    { method: "GET" }
  );

  if (!res.ok) {
    throw new Error(`Failed to fetch team info (${res.status})`);
  }

  return (await res.json()) as TeamInfoResponse;
}

/**
 * Get the playoff games for a specific season.
 * Assumes a GET /playoffs/{season_year} endpoint.
 */
export async function getPlayoffGames(year: number): Promise<PlayoffGame[]> {
  const res = await fetch(`${API_BASE_URL}/playoffs/${year}`, {
    method: "GET",
  });

  if (!res.ok) {
    throw new Error(`Failed to fetch playoff games (${res.status})`);
  }
  
  return handleResponse<PlayoffGame[]>(res);
}