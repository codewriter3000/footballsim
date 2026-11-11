/* @refresh reload */
import './index.css';
import { render } from 'solid-js/web';
import 'solid-devtools';

import App from './App';
import { Router } from '@solidjs/router';
import { SeasonProvider } from './SeasonContext';

const root = document.getElementById('root');

if (import.meta.env.DEV && !(root instanceof HTMLElement)) {
  throw new Error(
    'Root element not found. Did you forget to add it to your index.html? Or maybe the id attribute got misspelled?',
  );
}

render(
  () => (
    <SeasonProvider initialSeason={2029}>
      <Router>
        <App />
      </Router>
    </SeasonProvider>
  ),
  document.getElementById("root")!
);
