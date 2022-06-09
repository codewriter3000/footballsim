import React from 'react';
import {Col, Container, ProgressBar, Row} from "react-bootstrap";
import PlayerRow from "./PlayerRow";
import FirstNamesPregenerated from "../pregenerated_objects/FirstNamesPregenerated";
import LastNamesPregenerated from "../pregenerated_objects/LastNamesPregenerated";
import HomeStatePregenerated from "../pregenerated_objects/HomeStatePregenerated";
import {createRoot} from "react-dom";

const ReactDOM = require('react-dom');

class PlayerTable extends React.Component {

    constructor(props) {
        super(props);
        this.state = {playerNum: props.playerNum}
    }

    showPlayersInTable(players) {
        return players.map((player) => <PlayerRow key={player.key} firstName={player.firstName}
                                                  lastName={player.lastName}
                                                  homeState={player.homeState}/>);
    }

    generatePlayers = (num) => {
        const firstNames = new FirstNamesPregenerated();
        const lastNames = new LastNamesPregenerated();
        const homeStates = new HomeStatePregenerated();
        let players = [];
        for (let i = 0; i < num; i++) {
            players.push(
                {
                    "key": i,
                    "firstName": firstNames.getRandom(),
                    "lastName": lastNames.getRandom(),
                    "homeState": homeStates.getRandom()
                });
            createRoot(<ProgressBar max={this.state.playerNum} now={i} />)
        }
        return players;
    }

    render() {
        return (
            <div>
                <Container className='table body'>
                    <Row>
                        <Col><h3>First Name</h3></Col>
                        <Col><h3>Last Name</h3></Col>
                        <Col><h3>Home State</h3></Col>
                    </Row>
                    {this.showPlayersInTable(
                        this.generatePlayers(
                            this.state.playerNum
                        ))}
                </Container>
            </div>
        );
    }
}

export default PlayerTable;