import {Container} from "react-bootstrap";
import PlayerGeneratorForm from "./components/PlayerGeneratorForm";

// todo: generate a list of random names on this table
function App() {

    return (
        <div>
            <Container>
                <PlayerGeneratorForm/>
            </Container>
        </div>
    )
}

export default App;
