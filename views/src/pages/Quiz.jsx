import Button from 'react-bootstrap/Button'
import Card from 'react-bootstrap/Card'
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import { useState } from 'react'

import QuizQuestion from '../components/QuizQuestion'

export default function Quiz(questions) {

    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
    const [isAnswered, setIsAnswered] = useState(false)

    const handleNextQuestion = () => {
        if (currentQuestionIndex < questions.length - 1) {
            setCurrentQuestionIndex(currentQuestionIndex + 1)
            setIsAnswered(false)
        }
    }


    return (
        <Card className='d-flex flex-row justify-content-center w-50 shadow-sm mt-3'>
            {/* <QuizQuestion question={questions[currentQuestionIndex]} isAnswered={isAnswered} setIsAnswered={setIsAnswered}/> */}
            <Container>
                <Row className='d-flex flex-row justify-content-between'>
                    <Col xs="auto">Question {currentQuestionIndex + 1} of {questions.length}</Col>
                    <Col xs="auto"><Button variant='primary' onClick={handleNextQuestion}>Next Question</Button></Col>
                </Row>
            </Container>
        </Card>
    )
}
