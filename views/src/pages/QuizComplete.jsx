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
    const results = state?.results || []

    const handlePlayAgain = () => {
        navigate('/quiz/setup')
    }

    return (
        // if no results, redirect to quiz setup
        (results.length === 0)
        ? <Navigate to='/quiz/setup' replace />
        : <Card className="d-flex flex-row w-50 shadow-sm mt-3 bg-dark">
            <Container>
                <Row className="d-flex flex-row m-3">
                    <Col className="text-center">
                        <h1>Quiz Complete!</h1>
                    </Col>
                </Row>
                <hr />
                <Row className="d-flex flex-row m-3">
                    <Col className="text-center">
                        <h3>Score: 3/5</h3>
                    </Col>
                </Row>
                <Row className="d-flex flex-row m-3">
                    <Col className="d-flex flex-row justify-content-center">
                        <Button onClick={() => {handlePlayAgain()}}>Play Again</Button>
                    </Col>
                </Row>
            </Container>
        </Card>
    )
}

export default QuizComplete