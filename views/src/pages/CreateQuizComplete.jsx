import Button from 'react-bootstrap/Button'
import Card from 'react-bootstrap/Card'
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'

import { useLocation, useNavigate, Navigate } from 'react-router-dom'

export default function CreateQuizComplete() {
        const location = useLocation()
        const questions = location.state.questions ?? []
        const navigate = useNavigate()
        
        return (
            // if there is no questions array, redirect to setup
            (questions.length === 0)
            ? <Navigate to='/quiz/create/setup' replace />
            : <Card className="d-flex flex-row w-75 shadow-sm mt-3">
                <Container>
                    <Row className="d-flex flex-row m-3">
                        <Col className="text-center">
                            <h1>Quiz Created!</h1>
                        </Col>
                    </Row>
                    <Row className="d-flex flex-row m-3">
                        <Col className="d-flex flex-row justify-content-center">
                            <Button onClick={() => navigate('/quiz/play', {state: {questions}})}>Play Quiz</Button>
                        </Col>
                    </Row>
                </Container>
            </Card>
        )
}