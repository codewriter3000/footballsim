import type { Component } from 'solid-js';
import { createSignal, onMount, Show, For, createResource } from 'solid-js';
import { simulateSeason, getSeason, listSeasons, getTeamInfo, LeagueData } from './api';
import { addTeamRatings } from './rankings';
import { Route, A, useParams } from '@solidjs/router';
import { TeamDetails } from './TeamDetails';


const App: Component = () => {
  const [league, setLeague] = createSignal<LeagueData | null>(null);
  const [error, setError] = createSignal<boolean>(false);
  const [seasonYear] = createSignal<number>(2025);
  const [champion, setChampion] = createSignal<string | null>(null);

  onMount(async () => {
    const data = await getSeason(seasonYear()).catch(() => null);
    if (!data || !('playoff_games' in data)) {
      setError(true);
      return;
    }
    const championshipGame = data.playoff_games.at(-1);
    if (championshipGame) {
      setChampion(
        championshipGame.away_score > championshipGame.home_score
          ? championshipGame.home
          : championshipGame.away
      );
    } else {
      setChampion(null);
    }
    setLeague(addTeamRatings(data));
  });

  const sortedTeams = () => {
    const data = league();
    if (!data) return [];
    // If addTeamRatings is not adding .rating, fallback to 0
    return [...data.teams].sort((a: any, b: any) => (b.rating ?? 0) - (a.rating ?? 0));
  };


  // Home route component
  const Home = () => (
    <>
      <h1>State League Simulator</h1>
      <Show when={error()}>
        <p style={{ color: 'red', 'margin-top': '0.5rem' }}>Error: {error()}</p>
      </Show>
      <Show when={league()} keyed>
        {(data: LeagueData) => (
          <>
            <h2 style={{ 'margin-top': '1.5rem' }}>
              Season {data.season_year} Results
            </h2>
            <p>
              Champion: <strong>{champion()}</strong>
            </p>
            <h3>Standings</h3>
            <div>
              <table>
                <thead>
                  <tr>
                    <th>Rank</th>
                    <th>Team</th>
                    <th>Division</th>
                    <th>W-L</th>
                    <th>Rating</th>
                  </tr>
                </thead>
                <tbody>
                  <For each={sortedTeams()}>
                    {(t: any, i: () => number) => (
                      <tr>
                        <td>{i() + 1}</td>
                        <td>
                          <A href={`/team/${encodeURIComponent(t.name)}`}>{t.name}</A>
                        </td>
                        <td>{t.division}</td>
                        <td>
                          {t.wins}-{t.losses}-{t.ties}
                        </td>
                        <td>{Math.round((t.rating ?? 0) * 100) / 100}</td>
                      </tr>
                    )}
                  </For>
                </tbody>
              </table>
            </div>
          </>
        )}
      </Show>
    </>
  );

  // TeamDetails route wrapper (sync component using createResource)
  const TeamDetailsRoute = () => {
    const params = useParams();

    const [teamData] = createResource(
      () => params.name, // must stay inline like this
      async (name) => {
        console.log("Fetching:", name);
        return name ? await getTeamInfo(2025, name) : null;
      }
    );

    return (
      <Show when={!teamData.loading} fallback={<div>Loading...</div>}>
        <Show when={teamData()} fallback={<div>Team not found</div>}>
          <TeamDetails team={teamData()!.team} games={teamData()!.games} />
        </Show>
      </Show>
    );
  };

  return (
    <>
      <Route path="/" component={Home} />
      <Route path="/team/:name" component={TeamDetailsRoute} />
    </>
  );
};

export default App;
