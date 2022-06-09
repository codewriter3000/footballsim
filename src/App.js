import {Container} from "react-bootstrap";
import PlayerTable from "./components/PlayerTable";
import PlayerGeneratorForm from "./components/PlayerGeneratorForm";

// todo: generate a list of random names on this table
function App() {

    return (
        <div>
            <Container>
                <PlayerGeneratorForm/>
                <PlayerTable/>
            </Container>
        </div>
    )
}

export default App;
