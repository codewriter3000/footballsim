import { For } from "solid-js";
import { PlayoffGame } from "./components/PlayoffGame";

export const Playoffs = (playoffs: any) => {
    return (<>
        <h1>Playoffs</h1>
        <div style="display: flex; gap: 1rem;">
            <div>
                <For each={playoffs.filter((g: any) => g.round === "Round 1")}>
                    {(game) => (
                        <PlayoffGame game={game} round={1} />
                    )}
                </For>
            </div>
            <div style="margin-top: 4.5rem;">
                <For each={playoffs.filter((g: any) => g.round === "Round 2")}>
                    {(game) => (
                        <PlayoffGame game={game} round={2} />
                    )}
                </For>
            </div>
            <div style="margin-top: 13.5rem;">
                <For each={playoffs.filter((g: any) => g.round === "Round 3")}>
                    {(game) => (
                        <PlayoffGame game={game} round={3} />
                    )}
                </For>
            </div>
            <div style="margin-top: 31.5rem;">
                <For each={playoffs.filter((g: any) => g.round === "Round 4")}>
                    {(game) => (
                        <PlayoffGame game={game} round={4} />
                    )}
                </For>
            </div>      
        </div>
    </>);
};