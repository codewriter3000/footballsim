import { A } from "@solidjs/router";
import { useSeason } from "../SeasonContext";

export const Header = () => {
  const { season, setSeason } = useSeason();

  return (
    <div style="padding: 1rem; color: white; text-align: center;">
      <h1>Football League Simulator</h1>

      <div style="margin-bottom: 0.75rem; display: flex; gap: 0.5rem; justify-content: center; align-items: center;">
        <span>Season:</span>

        <button
          onClick={() => setSeason((s) => Math.max(1900, s - 1))}
          style="padding: 0.25rem 0.5rem;"
          aria-label="Previous season"
        >
          −
        </button>

        <input
          type="number"
          min="1900"
          max="2100"
          value={season()}
          onInput={(e) => {
            const n = parseInt(e.currentTarget.value, 10);
            if (!Number.isNaN(n)) setSeason(n);
          }}
          style="width: 6rem; padding: 0.25rem; text-align: center;"
        />

        <button
          onClick={() => setSeason((s) => Math.min(2100, s + 1))}
          style="padding: 0.25rem 0.5rem;"
          aria-label="Next season"
        >
          +
        </button>
      </div>

      <A href="/" style="text-decoration: none; margin-right: 1rem;">
        Standings
      </A>

      <A href={`/playoffs/${season()}`} style="text-decoration: none;">
        Playoffs
      </A>
    </div>
  );
};