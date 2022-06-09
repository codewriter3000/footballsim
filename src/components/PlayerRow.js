import {Col, Row} from 'react-bootstrap';

function PlayerRow(props) {
    return (
        <Row>
            <Col>{props.firstName}</Col>
            <Col>{props.lastName}</Col>
            <Col>{props.homeState}</Col>
        </Row>
    );
}

export default PlayerRow;