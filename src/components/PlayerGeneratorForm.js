import React from 'react';
import {Alert, Button, Container, Form, FormControl, FormGroup, FormLabel} from "react-bootstrap";
import PlayerTable from "./PlayerTable";

class PlayerGeneratorForm extends React.Component {

    constructor(props) {
        super(props);
        this.state = {playerNum: 50,
            playerNumTooSmall: false,
            generated: false,
            editEnabled: false,
            submitEnabled: true};
    }

    handleSubmit = (event) => {
        event.preventDefault();
        if(!this.state.playerNumTooSmall){
            this.setState({generated: true,
            editEnabled: true,
            submitEnabled: false});
        }
    }

    changePlayerNum = (event) => this.setState(
    {playerNum: event.target.value,
        playerNumTooSmall: event.target.value < 1}
    );

    handleEdit = () => {
        this.setState(
            {editEnabled: false,
            submitEnabled: true,
            generated: false}
        );
    }

    render() {
        return (
            <Container className='body'>
                <Form onSubmit={this.handleSubmit}>
                    <h3>Player Generator</h3>
                    <FormGroup className='mb-4 d-inline-block p-2'>
                        <FormLabel htmlFor='numberOfPlayers'>Number of Players</FormLabel>
                        <FormControl className='numberBox' name='numberOfPlayers'
                                     type='number' placeholder='Enter number' defaultValue='50'
                                     onChange={this.changePlayerNum} disabled={this.state.editEnabled}/>
                        {this.state.playerNumTooSmall &&
                            <Alert id='playerNumTooSmall' variant='danger' >
                                Number of Players must be at least 1.</Alert>}
                    </FormGroup>
                    <div>
                        <Button className='button' onClick={this.handleEdit} disabled={!this.state.editEnabled}>Edit</Button>
                        <Button className='button' type='submit' disabled={!this.state.submitEnabled}>Submit</Button>
                    </div>
                </Form>
                {this.state.generated && <PlayerTable playerNum={this.state.playerNum}/>}
            </Container>
        )
    }
}

export default PlayerGeneratorForm;