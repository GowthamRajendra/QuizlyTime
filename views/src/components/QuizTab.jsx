import Card from 'react-bootstrap/Card'
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

// Display a quiz tab with the title, score, total questions, and timestamp
// Used in profile page to display play history
// Used in play page to display user created quizzes
function QuizTab({title, score=null, total_questions, timestamp}) {
    return (
        <Card className='w-100'>
            <Card.Body>
                <Row className="align-items-center justify-content-between">
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
                    { // score is null for quizzes in play page
                    (score == null)
                    ? null
                    :<Col xs="auto">
                        <Card.Title>
                            {Math.round(score / (total_questions * 10) * 100)}%
                        </Card.Title>
                        <Card.Text>
                            {score} / {total_questions * 10}
                        </Card.Text>
                    </Col>
                    }
                </Row>
            </Card.Body>
        </Card>
    );
}

export default QuizTab;