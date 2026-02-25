import { A } from "@solidjs/router"

export const PlayoffGame = ({ game, round }) => {
    return (
        <div style={`background-color: #393939;
                    padding: 1rem;
                    border-radius: 8px; 
                    height: 8rem; 
                    display: flex; 
                    margin-bottom: ${round === 1 ? 1 : round === 2 ? 10 : round === 3 ? 28 : 32}rem;
                    flex-direction: column;
                    justify-content: center;`}>
            {game.away_score > game.home_score ? <u><A style="color: inherit;" href={`/team/${encodeURIComponent(game.away)}`}>#{game.away_seed} {game.away} ({game.away_score})</A></u> : <A style="color: inherit;" href={`/team/${encodeURIComponent(game.away)}`}>#{game.away_seed} {game.away} ({game.away_score})</A>}<br />
            @<br />
            {game.home_score > game.away_score ? <u><A style="color: inherit;" href={`/team/${encodeURIComponent(game.home)}`}>#{game.home_seed} {game.home} ({game.home_score})</A></u> : <A style="color: inherit;" href={`/team/${encodeURIComponent(game.home)}`}>#{game.home_seed} {game.home} ({game.home_score})</A>}
        </div>
    )
}