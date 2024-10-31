import Button from 'react-bootstrap/Button'
import Card from 'react-bootstrap/Card'
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import 'bootstrap-icons/font/bootstrap-icons.css'

import { useEffect, useState } from 'react'
import { useLocation, useNavigate, Navigate } from 'react-router-dom'

// Quiz game page.
// Handles communication with server to get questions and check answers.
// Renders questions and choices.

export default function Quiz() {
    // Questions from QuizSetup
    const { state } = useLocation()
    const questions = state?.questions || []

    // Display current question
    const [questionIndex, setQuestionIndex] = useState(0)
    const currQuestion = questions[questionIndex]

    // User selected answer
    const [selected, setSelected] = useState(null)

    // Correct answer
    const [correct, setCorrect] = useState(null)

    const navigate = useNavigate()

    const handleSubmit = () => {
        if (selected === null) {
            alert('Please select an answer.')
            return
        }
        else {
            setSelected(null)
        }

        // Check if answer is correct
        // Display correct/incorrect
        // socket event to server
        // setCorrect(selected)

        // Move to next question
        // If last question, move to results page
        if (questionIndex < questions.length - 1) {
            setQuestionIndex(questionIndex + 1)
        }
        else {
            navigate('/quiz/results')
        }
    }

    function buttonColor(index) {
        if (index === correct) {
            return 'success'
        }
        else if (index === selected && correct !== null) {
            return 'danger'
        }
        else if (index === selected) {
            return 'primary'
        }
        else {
            return 'outline-primary'
        }
    }

    function resultIcon(index) {
        if (correct !== null) {
            if (index === correct) {
                return <i className="bi bi-check-circle-fill position-absolute end-0 me-5"></i>
            }
            else if (index === selected) {
                return <i className="bi bi-x-circle-fill position-absolute end-0 me-5"></i>
            }
        }
    }

    return (
        // If no questions, redirect to setup page.
        (questions.length === 0)
        ? <Navigate to='/quiz/setup' replace />
          // Question card, with prompt and choices.
        : <Card className='d-flex flex-row justify-content-center w-50 shadow-sm mt-3 bg-dark'>
            <Container>
                <Row className='d-flex flex-row justify-content-center mx-3 mt-3'>
                    <h3>{currQuestion.number}. {currQuestion.prompt}</h3>
                </Row>
                <Row className='d-flex flex-row row-gap-3 mx-3 mt-3'>
                    {currQuestion.choices.map((choice, index) => {
                        return <Button key={index} 
                        variant={buttonColor(index)} 
                        onClick={() => setSelected(index)}>
                            {choice} 
                            {resultIcon(index)}
                        </Button>
                    })}
                </Row>
                <hr />
                <Row className='d-flex flex-row justify-content-between align-items-center mb-3'>
                    <Col xs="auto">Question {questionIndex+1} of {questions.length}</Col>
                    <Col xs="auto"><Button variant='primary' onClick={() => {handleSubmit()}}>Submit</Button></Col>
                </Row>
            </Container>
        </Card>
    )
}
