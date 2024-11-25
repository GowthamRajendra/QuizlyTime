import Card from 'react-bootstrap/Card'
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

function QuizTab({title, score, total_questions, timestamp}) {
    return (
        <Card>
            <Card.Body>
                <Row>
                    <Col>
                        <Card.Title>{title}</Card.Title>
                        <Card.Subtitle className='text-muted'>
                            {timestamp}
                        </Card.Subtitle>
                    </Col>
                    <Col>
                        <Card.Title>
                            {total_questions} Questions
                        </Card.Title>
                    </Col>
                    <Col>
                        <Card.Title>
                            {Math.round(score / (total_questions * 10) * 100)}%
                        </Card.Title>
                        <Card.Text>
                            {score} / {total_questions * 10}
                        </Card.Text>
                    </Col>
                </Row>
            </Card.Body>
        </Card>
    );
}

export default QuizTab;