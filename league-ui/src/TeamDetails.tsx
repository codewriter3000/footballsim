import { Game, TeamStats } from "./api";
import { Component, For, Show, createResource } from "solid-js";
import { A } from "@solidjs/router";

type TeamDetailsProps = {
  team: TeamStats;
  games: Game[];
};

export const TeamDetails: Component<TeamDetailsProps> = (props) => {
  const { team, games } = props;

  console.log("TeamDetails props:", { team, games });

  return (
    <>
      <div>
        <h1>{team.name}</h1>
        <p>Division: {team.division}</p>
        <p>Record: {team.wins}-{team.losses}-{team.ties}</p>
        <p>Points For: {team.points_for}</p>
        <p>Points Against: {team.points_against}</p>
        <p>Strength of Schedule: {typeof team.sos === "number" ? team.sos.toFixed(3) : "N/A"}</p>
      </div>

      <div>
        <h2>Games</h2>
		<Show
          when={games && games.length > 0}
          fallback={<p>No games found.</p>}
        >
			<table>
				<thead>
					<tr>
						<th>Week</th>
						<th>Opponent</th>
						<th>Result</th>
						<th>Score</th>
					</tr>
				</thead>
				<tbody>
					<For each={games}>
						{(g) => (
							<tr>
								<Show when={g.home === team.name}>
									<td>{g.week}</td>
									<td><A href={`/team/${encodeURIComponent(g.away)}`}>{g.away}</A></td>
									<td>{g.away_score === g.home_score ? "T" : g.away_score > g.home_score ? "L" : "W"}</td>
									<td>{g.home_score + " - " + g.away_score}</td>
								</Show>
								<Show when={g.away === team.name}>
									<td>{g.week}</td>
									<td><A href={`/team/${encodeURIComponent(g.home)}`}>{g.home}</A></td>
									<td>{g.home_score === g.away_score ? "T" : g.home_score > g.away_score ? "L" : "W"}</td>
									<td>{g.away_score + " - " + g.home_score}</td>
								</Show>
							</tr>
						)}
					</For>
				</tbody>
			</table>
        </Show>
      </div>
    </>
  );
};
