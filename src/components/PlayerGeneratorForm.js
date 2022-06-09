import React from 'react';
import {Alert, Button, Container, Form, FormControl, FormGroup, FormLabel} from "react-bootstrap";

class PlayerGeneratorForm extends React.Component {

    constructor(props) {
        super(props);
        this.state = {playerNum: 50, playerNumTooSmall: false};
    }

    handleSubmit = (event) => {
        // event.preventDefault();
        if(!this.state.playerNumTooSmall){
            localStorage.setItem('playerNum', this.state.playerNum);
        }
        // PlayerTable.generatePlayers(this.state.playerNum);
    }

    changePlayerNum = (event) => this.setState({playerNum: event.target.value, playerNumTooSmall: event.target.value < 1});

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
                            <Alert id='playerNumTooSmall' variant='danger' >Number of Players must be at least 1.</Alert>}
                    </FormGroup>
                    <div>
                        <Button type='submit'>Submit</Button>
                    </div>
                </Form>
            </Container>
        )
    }
}

export default PlayerGeneratorForm;