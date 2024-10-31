import Button from 'react-bootstrap/Button'
import Card from 'react-bootstrap/Card'
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import 'bootstrap-icons/font/bootstrap-icons.css'
import { useEffect, useState } from 'react'
import { useLocation, useNavigate, Navigate } from 'react-router-dom'
import useAuth from '../hooks/useAuth';

import io from 'socket.io-client'

// import useAxios from '../hooks/useAxios'

export default function Quiz() {
    const { auth } = useAuth()

    // Get questions from setup page
    const location = useLocation()
    const questions = location.state.questions

    // server connection
    const [socket, setSocket] = useState(null)

    // Display current question
    const [questionIndex, setQuestionIndex] = useState(0)
    const currQuestion = questions[questionIndex]

    // User selected answer
    const [selected, setSelected] = useState(null)
    const [submitted, setSubmitted] = useState(false)

    // Correct answer
    const [correct, setCorrect] = useState(null)

    const navigate = useNavigate()

    const handleSubmit = () => {
        if (selected === null) {
            alert('Please select an answer.')
            return
        }
        else {
            setSubmitted(true)
        }
        // else {
        //     setSelected(null)
        // }

        // Check if answer is correct
        // Display correct/incorrect
        // socket event to server
        console.log(`email: ${auth.email}, question_id: ${currQuestion.question_id}, user_answer: ${currQuestion.choices[selected]}`);
        socket.emit('check_answer', { "email": auth.email,  "question_id": currQuestion.question_id, "user_answer": currQuestion.choices[selected], "question_index": questionIndex})
        console.log('emitted');

        setTimeout(() => {
            console.log('displaying correct answer...');
            setSubmitted(false)

            // Move to next question
            // If last question, move to results page
            if (questionIndex < questions.length - 1) {
                setQuestionIndex(questionIndex + 1)
            }
            setCorrect(null)
        }, 2000)
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

    useEffect(() => {
        // Connect to the server
        const newSocket = io('http://localhost:5000')
        setSocket(newSocket)
        
        newSocket.on('answer_checked', ({correct_answer, question_index}) => {
            console.log('answer checked');
            console.log(`correct: ${correct_answer}, ${question_index}`);
            console.log(questions[question_index].choices)
            setCorrect(questions[question_index].choices.indexOf(correct_answer))
        })        

        newSocket.on('quiz_completed', ({score}) => {
            console.log(`quiz completed: ${score}`);
            navigate('/quiz/results', {state: {score: score, total: questions.length}})
        });

        // Clean up. Remove the event listener when the component is unmounted
        return () => {
            newSocket.disconnect()
        }
    }, [])

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
                    <h3>{questionIndex+1}. {currQuestion.prompt}</h3>
                </Row>
                <Row className='d-flex flex-row row-gap-3 mx-3 mt-3'>
                    {currQuestion.choices.map((choice, index) => {
                        return <Button key={index} 
                        variant={buttonColor(index)} 
                        onClick={() => setSelected(index)}
                        disabled={submitted}>
                            {choice} 
                            {resultIcon(index)}
                        </Button>
                    })}
                </Row>
                <hr />
                <Row className='d-flex flex-row justify-content-between align-items-center mb-3'>
                    <Col xs="auto">Question {questionIndex+1} of {questions.length}</Col>
                    <Col xs="auto"><Button variant='primary' 
                    onClick={() => {handleSubmit()}} 
                    disabled={submitted}>Submit</Button></Col>
                </Row>
            </Container>
        </Card>
    )
}
