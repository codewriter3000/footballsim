import type { Component } from 'solid-js';
import { createSignal, onMount } from 'solid-js';
import { simulateSeason, getSeason, listSeasons, LeagueData } from './api';
import { addTeamRatings } from './rankings.ts';

const App: Component = () => {
	const [league, setLeague] = createSignal<LeagueData | null>(null);
	const [error, setError] = createSignal<boolean>(false);
	const [seasonYear, setSeasonYear] = createSignal<int>(2025);
	const [champion, setChampion] = createSignal<string>(null);

	onMount(async () => {
		const data = await getSeason(seasonYear()).catch(() => []);
		//setLeague(data);
		const championshipGame = data.playoff_games.at(-1); 
		setChampion(
			championshipGame.awayScore > championshipGame.homeScore ? championshipGame.home : championshipGame.away
		);
		setLeague(addTeamRatings(data));
	});

	const run = async () => {
		const data = await simulateSeason({ seasonYear: 2025 });
		setLeague(data);
	};

  const sortedTeams = () => {
    const data = league();
    if (!data) return [];
    // Backend already has full stats on `teams`, so just format them
    return [...data.teams].sort((a, b) => {
			return b.rating - a.rating;
    });
  };

  return (
    <div>
      <h1>State League Simulator</h1>

      <Show when={error()}>
        <p style={{ color: "red", "margin-top": "0.5rem" }}>
          Error: {error()}
        </p>
      </Show>

      <Show when={league()}>
        {(data) => (
          <>
            <h2 style={{ "margin-top": "1.5rem" }}>
              Season {data().season_year} Results
            </h2>
            <p>
              Champion:{" "}
              <strong>{champion()}</strong>
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
                    {(t: any, i) => {
                      const games =
                        t.wins + t.losses + t.ties;
                      const diff = t.points_for - t.points_against;
                      return (
                        <tr>
													<td>{i() + 1}</td>
                          <td>{t.name}</td>
                          <td>{t.division}</td>
                          <td>
                            {t.wins}-{t.losses}-{t.ties}
                          </td>
													<td>
														{Math.round(t.rating * 100) / 100}
													</td>
                        </tr>
                      );
                    }}
                  </For>
                </tbody>
              </table>
            </div>
          </>
        )}
      </Show>
    </div>
  );
};

export default App;
