import { A } from "@solidjs/router"

export const Header = () => {
    return (
        <div style="padding: 1rem; color: white; text-align: center;">
            <h1>Football League Simulator</h1>
            <A href="/" style="text-decoration: none; margin-right: 1rem;">Standings</A>
            <A href="/playoffs/2025" style="text-decoration: none;">Playoffs</A>
        </div>
    )
}