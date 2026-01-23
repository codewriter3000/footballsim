export const addTeamRatings = (league: any) => {
	const teams = [...league.teams];
	const regular_season_games = [...league.regular_season_games];

	for (const team of teams) {
		let team_games = [];
		for (const game of regular_season_games) {
			if (game.away === team.name) {
				team_games = [...team_games, {...game, opponent: game.home, opponentScore: game.home_score, myScore: game.away_score}];
			} else if (game.home === team.name) {
				team_games = [...team_games, {...game, opponent: game.away, opponentScore: game.away_score, myScore: game.home_score}];
			}
		}

		const rawPts = team_games.reduce((acc, curr) => {
			const my = Number(curr.myScore);
			const opp = Number(curr.opponentScore);

			if (!Number.isFinite(my) || !Number.isFinite(opp)) {
				// Either log or skip bad data
				return acc;
			}

			const diff = opp - my;

			// Skip ties but keep accumulated value
			if (diff === 0) return acc;

			const magnitude = Math.min(Math.max(Math.abs(diff), 15), 30);

			// If you actually want negative for losses, positive for wins:
			const sign = diff > 0 ? -1 : 1; // opp > me => loss => negative

			return acc + magnitude * sign * teams.find(t => t.name === curr.opponent).sos;
		}, 0);

		team['rating'] = rawPts;
	}

	return league;
};
