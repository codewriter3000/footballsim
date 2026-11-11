import { createContext, useContext, ParentComponent, createSignal, Accessor, Setter } from "solid-js";

type SeasonContextValue = {
  season: Accessor<number>;
  setSeason: Setter<number>;
};

const SeasonContext = createContext<SeasonContextValue>();

export const SeasonProvider: ParentComponent<{ initialSeason?: number }> = (props) => {
  const [season, setSeason] = createSignal(props.initialSeason ?? 2029);

  return (
    <SeasonContext.Provider value={{ season, setSeason }}>
      {props.children}
    </SeasonContext.Provider>
  );
};

export const useSeason = () => {
  const ctx = useContext(SeasonContext);
  if (!ctx) throw new Error("useSeason must be used within <SeasonProvider>");
  return ctx;
};