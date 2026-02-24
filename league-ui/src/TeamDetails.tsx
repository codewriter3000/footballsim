import { Game, PlayoffGame, TeamStats } from "./api";
import { Component, For, Show, createResource } from "solid-js";
import { A } from "@solidjs/router";

type TeamDetailsProps = {
  team: TeamStats;
  regularSeasonGames: Game[];
  postseasonGames: PlayoffGame[];
};

export const TeamDetails: Component<TeamDetailsProps> = (props) => {
  const { team, regularSeasonGames, postseasonGames } = props;

  console.log("TeamDetails props:", { team, regularSeasonGames, postseasonGames });

  const playoffGames = postseasonGames.filter(g => !g.round.startsWith("C") && !g.round.startsWith("PC"));
  const crossoverGames = postseasonGames.filter(g => g.round.startsWith("C"));
  const consolationGames = postseasonGames.filter(g => g.round.startsWith("PC"));

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
		<h3>Regular Season</h3>
		<Show
          when={regularSeasonGames && regularSeasonGames.length > 0}
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
					<For each={regularSeasonGames}>
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
		<Show
			when={crossoverGames && crossoverGames.length > 0}
			fallback={<></>}
		>
			<h3 class="mt-2">Crossover Games</h3>
			<table>
				<thead>
					<tr>
						<th>Round</th>
						<th>Opponent</th>
						<th>Result</th>
						<th>Score</th>
					</tr>
				</thead>
				<tbody>
					<For each={crossoverGames}>
						{(g) => (
							<tr>
								<Show when={g.home === team.name}>
									<td>{g.round}</td>
									<td><A href={`/team/${encodeURIComponent(g.away)}`}>{g.away}</A></td>
									<td>{g.away_score === g.home_score ? "T" : g.away_score > g.home_score ? "L" : "W"}</td>
									<td>{g.home_score + " - " + g.away_score}</td>
								</Show>
								<Show when={g.away === team.name}>
									<td>{g.round}</td>
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
		<h3 class="mt-2">Playoffs</h3>
		<Show
          when={playoffGames && playoffGames.length > 0}
          fallback={<p>Did not qualify for the playoffs.</p>}
        >
			<table>
				<thead>
					<tr>
						<th>Round</th>
						<th>Opponent</th>
						<th>Result</th>
						<th>Score</th>
					</tr>
				</thead>
				<tbody>
					<For each={playoffGames}>
						{(g) => (
							<tr>
								<Show when={g.home === team.name}>
									<td>{g.round}</td>
									<td><A href={`/team/${encodeURIComponent(g.away)}`}>{g.away}</A></td>
									<td>{g.away_score === g.home_score ? "T" : g.away_score > g.home_score ? "L" : "W"}</td>
									<td>{g.home_score + " - " + g.away_score}</td>
								</Show>
								<Show when={g.away === team.name}>
									<td>{g.round}</td>
									<td><A href={`/team/${encodeURIComponent(g.home)}`}>{g.home}</A></td>
									<td>{g.home_score === g.away_score ? "T" : g.home_score > g.away_score ? "L" : "W"}</td>
									<td>{g.away_score + " - " + g.home_score}</td>
								</Show>
							</tr>
						)}
					</For>
				</tbody>
			</table>
			<Show
				when={consolationGames && consolationGames.length > 0}
				fallback={<p></p>}
			>
				<h3 class="mt-2">Consolation Games</h3>
				<table>
					<thead>
						<tr>
							<th>Round</th>
							<th>Opponent</th>
							<th>Result</th>
							<th>Score</th>
						</tr>
					</thead>
					<tbody>
						<For each={consolationGames}>
							{(g) => (
								<tr>
									<Show when={g.home === team.name}>
										<td>{g.round}</td>
										<td><A href={`/team/${encodeURIComponent(g.away)}`}>{g.away}</A></td>
										<td>{g.away_score === g.home_score ? "T" : g.away_score > g.home_score ? "L" : "W"}</td>
										<td>{g.home_score + " - " + g.away_score}</td>
									</Show>
									<Show when={g.away === team.name}>
										<td>{g.round}</td>
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
        </Show>
      </div>
    </>
  );
};
