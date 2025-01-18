import { useNavigate, useLocation, Navigate } from "react-router-dom"
import Card from 'react-bootstrap/Card'
import Button from 'react-bootstrap/Button'
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'

// Page displays the results of the quiz

function QuizComplete() {
    const navigate = useNavigate()
    const { state } = useLocation()
    const score = state?.score ?? null
    const total = state?.total ?? 0

    return (
        // if no score, redirect to quiz setup (because something went wrong)
        (score === null)
        ? <Navigate to='/quiz/setup' replace />
        : <Card className="d-flex flex-row col-11 col-lg-4 shadow-sm mt-3">
            <Container>
                <Row className="d-flex flex-row m-3">
                    <Col className="text-center">
                        <h1>Quiz Complete!</h1>
                    </Col>
                </Row>
                <hr />
                <Row className="d-flex flex-row m-3">
                    <Col className="text-center">
                        <h3>Score: {Math.floor(score)}/{total}</h3>
                    </Col>
                </Row>
                <Row className="d-flex flex-row m-3">
                    <Col className="d-flex flex-row justify-content-center">
                        <Button onClick={() => {navigate('/quiz')}}>Play Again</Button>
                    </Col>
                </Row>
            </Container>
        </Card>
    )
}

export default QuizComplete