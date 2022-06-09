import React from 'react';
import {Col, Container, Row} from "react-bootstrap";
import PlayerRow from "./PlayerRow";
import FirstNamesPregenerated from "../pregenerated_objects/FirstNamesPregenerated";
import LastNamesPregenerated from "../pregenerated_objects/LastNamesPregenerated";

class PlayerTable extends React.Component {

    showPlayersInTable(players) {
        return players.map((player) => <PlayerRow firstName={player.firstName} lastName={player.lastName}/>);
    }

    generatePlayers = (num) => {
        const firstNames = new FirstNamesPregenerated();
        const lastNames = new LastNamesPregenerated();
        let players = [];
        for (let i = 0; i < num; i++) {
            players.push(
                {
                    "firstName": firstNames.getRandom(),
                    "lastName": lastNames.getRandom()
                });
        }
        return players;
    }

    render() {
        return (
            <Container className='body'>
                <Row>
                    <Col><h3>First Name</h3></Col>
                    <Col><h3>Last Name</h3></Col>
                </Row>
                    {this.showPlayersInTable(
                        this.generatePlayers(
                            localStorage.getItem('playerNum') === undefined ? 0 : localStorage.getItem('playerNum')
                        ))}
            </Container>
        );
    }
}

export default PlayerTable;