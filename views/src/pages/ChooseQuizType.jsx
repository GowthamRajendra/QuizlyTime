import Card from 'react-bootstrap/Card'
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import 'bootstrap-icons/font/bootstrap-icons.css'
import '../quiz.css'

import { useNavigate } from 'react-router-dom'

export default function ChooseQuizType() {
    const navigate = useNavigate()

    return (
        <Container className="d-flex justify-content-center align-items-start">
            <Row className='w-100'>
                <Col className="d-flex justify-content-center col-12 col-lg-6">
                    <Card className="text-center clickable-card col-12" onClick={() => navigate('/quiz/setup')}>
                        <Card.Body>
                            <i className="bi bi-dice-5-fill" style={{fontSize:"7.5em"}}></i>
                            <Card.Title>Create Random Quiz</Card.Title>
                        </Card.Body>
                    </Card>
                </Col>
                <Col className="d-flex justify-content-center col-12 col-lg-6">
                    <Card className="text-center clickable-card col-12" onClick={() => navigate('/quiz/select')}>
                        <Card.Body>
                            <i className="bi bi-archive-fill" style={{fontSize:"7.5em"}}></i>
                            <Card.Title>Choose a Quiz</Card.Title>
                        </Card.Body>
                    </Card>
                </Col>
            </Row>
        </Container>
      );

}