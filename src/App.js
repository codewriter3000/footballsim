import PlayerRow from './components/PlayerRow';
import {Container} from "react-bootstrap";

// todo: generate a list of random names on this table
function App() {
  return (
      <Container className='body'>
          <PlayerRow firstName='Tom' lastName='Brady' />
          <PlayerRow firstName='Aaron' lastName='Rodgers' />
          <PlayerRow firstName='Josh' lastName='Allen' />
          <PlayerRow firstName='Patrick' lastName='Mahomes' />
      </Container>
  );
}

export default App;
