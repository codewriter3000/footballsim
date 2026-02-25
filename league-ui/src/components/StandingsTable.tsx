import { A } from "@solidjs/router";
import { For } from "solid-js";

export const StandingsTable = (props: { teams: any[], division: string }) => {
    return (
        <table>
            <caption>{props.division}</caption>
            <thead>
                <tr>
                <th>Rank</th>
                <th>Team</th>
                <th>W-L</th>
                <th>Rating</th>
                </tr>
            </thead>
            <tbody>
                <For each={props.teams.filter((t: any) => t.division === props.division)}>
                {(t: any, i: () => number) => (
                    <tr>
                    <td>{i() + 1}</td>
                    <td>
                        <A href={`/team/${encodeURIComponent(t.name)}`}>{t.name}</A>
                    </td>
                    <td>
                        {t.wins}-{t.losses}-{t.ties}
                    </td>
                    <td>{Math.round((t.rating ?? 0) * 100) / 100}</td>
                    </tr>
                )}
                </For>
            </tbody>
        </table>
    );
};