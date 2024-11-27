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
        <Container className="d-flex justify-content-center align-items-start vh-100 vw-100">
            <Row style={{marginTop: '1rem'}}>
                <Col md={6} className="d-flex justify-content-center">
                    <Card className="text-center clickable-card" style={{width: "18rem"}} onClick={() => navigate('/quiz/setup')}>
                        <Card.Body>
                            <i className="bi bi-dice-5-fill" style={{fontSize: '10rem'}}></i>
                            <Card.Title>Create Random Quiz</Card.Title>
                        </Card.Body>
                    </Card>
                </Col>
                <Col md={6} className="d-flex justify-content-center">
                    <Card className="text-center clickable-card" style={{width: "18rem"}} onClick={() => navigate('/quiz/select')}>
                        <Card.Body>
                            <i class="bi bi-archive-fill" style={{fontSize: '10rem'}}></i>
                            <Card.Title>Choose a Quiz</Card.Title>
                        </Card.Body>
                    </Card>
                </Col>
            </Row>
        </Container>
      );

}