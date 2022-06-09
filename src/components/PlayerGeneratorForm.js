import React from 'react';
import {Alert, Button, Container, Form, FormControl, FormGroup, FormLabel} from "react-bootstrap";
import PlayerTable from "./PlayerTable";

class PlayerGeneratorForm extends React.Component {

    constructor(props) {
        super(props);
        this.state = {playerNum: 50, playerNumTooSmall: false, generated: false};
    }

    _playerNum;

    set playerNum(playerNum) {
        this._playerNum = playerNum;
    }

    get playerNum() {
        return this._playerNum;
    }

    handleSubmit = (event) => {
        event.preventDefault();
        if(!this.state.playerNumTooSmall){
            this.playerNum = this.state.playerNum;
            this.setState({generated: true});
        }
    }

    changePlayerNum = (event) => this.setState(
        {playerNum: event.target.value,
            playerNumTooSmall: event.target.value < 1,
            generated: false});

    render() {
        return (
            <Container className='body'>
                <Form onSubmit={this.handleSubmit}>
                    <h3>Player Generator</h3>
                    <FormGroup className='mb-4 d-inline-block p-2'>
                        <FormLabel htmlFor='numberOfPlayers'>Number of Players</FormLabel>
                        <FormControl className='numberBox' name='numberOfPlayers'
                                     type='number' placeholder='Enter number' defaultValue='50'
                                     onChange={this.changePlayerNum}/>
                        {this.state.playerNumTooSmall &&
                            <Alert id='playerNumTooSmall' variant='danger' >
                                Number of Players must be at least 1.</Alert>}
                    </FormGroup>
                    <div>
                        <Button type='submit'>Submit</Button>
                    </div>
                </Form>
                {this.state.generated && <PlayerTable playerNum={this.playerNum}/>}
            </Container>
        )
    }
}

export default PlayerGeneratorForm;